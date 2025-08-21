import json
import random
import re
from typing import Dict, List

import google.generativeai as genai
from groq import Groq
from huggingface_hub import InferenceClient
from mistralai import Mistral

from api.config import settings


class PIIDetection:
    def __init__(
        self,
        has_pii: bool,
        detected_types: List[str],
        confidence: float,
        filtered_message: str,
        reasoning: str,
        provider: str,
    ):
        self.has_pii = has_pii
        self.detected_types = detected_types
        self.confidence = confidence
        self.filtered_message = filtered_message
        self.reasoning = reasoning
        self.provider = provider


class ContentFilterService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContentFilterService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.llm_providers = [
            self._groq_provider,
            self._gemini_provider,
            self._huggingface_provider,
            self._mistral_provider,
        ]
        self._initialized = True

    def _manual_filter(self, message: str) -> Dict:
        normalized_message = "".join(message.split())
        # Email
        if re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", normalized_message
        ):
            return {"filtered": True, "reason": "EMAIL_ADDRESS"}
        # More specific phone number
        if re.search(r"(\+65)?[689]\d{7}", normalized_message):
            return {"filtered": True, "reason": "PHONE_NUMBER"}
        # Unit number
        if re.search(
            r"#\d{2,}-\d{2,}|unit#\d{2,}-\d{2,}", normalized_message, re.IGNORECASE
        ):
            return {"filtered": True, "reason": "UNIT_NUMBER"}
        # NRIC (more specific than postal code)
        if re.search(r"[STFGstfg]\d{7}[A-Za-z]", normalized_message):
            return {"filtered": True, "reason": "SG_NRIC"}
        # Postal code with context
        if re.search(r"(singapore|s)\d{6}", normalized_message, re.IGNORECASE):
            return {"filtered": True, "reason": "POSTAL_CODE"}
        # Postal code
        if re.search(r"\d{6}", normalized_message):
            return {"filtered": True, "reason": "POSTAL_CODE"}
        # Phone number
        if re.search(r"\d{8}", normalized_message):
            return {"filtered": True, "reason": "PHONE_NUMBER"}
        # Address keywords with number
        if re.search(
            r"\b(road|rd|blk|block|street|st)\b", message, re.IGNORECASE
        ) and re.search(r"\d", message):
            return {"filtered": True, "reason": "ADDRESS"}
        return {"filtered": False}

    async def filter_message(self, message: str, threshold: float = 0.7) -> Dict:
        manual_filter_result = self._manual_filter(message)
        if manual_filter_result["filtered"]:
            return {
                "filtered": True,
                "content": f"Message filtered due to potential PII: {manual_filter_result['reason']}",
                "detected": [manual_filter_result["reason"]],
                "confidence": 1.0,
                "reasoning": "Message flagged by manual filter.",
                "provider": "manual_filter",
            }

        if len(message) < 10:
            return {
                "filtered": False,
                "content": message,
                "detected": [],
                "confidence": 0.0,
                "reasoning": "Message is too short to be processed by LLM.",
                "provider": "manual_filter",
            }

        random.shuffle(self.llm_providers)

        last_exception = None
        for provider in self.llm_providers:
            try:
                result = await provider(message, threshold)
                if "Failed to parse" in result.get("reasoning", ""):
                    last_exception = Exception(
                        f"Provider {result.get('provider')} failed to parse output."
                    )
                    continue
                return result
            except Exception as e:
                last_exception = e
                continue

        if last_exception:
            raise last_exception

        raise Exception("All LLM providers failed to filter the message.")

    async def _groq_provider(self, message: str, threshold: float) -> Dict:
        client = Groq(api_key=settings.groq_api_key)
        return self._get_llm_response(
            client, message, "llama-3.1-8b-instant", threshold, message
        )

    async def _gemini_provider(self, message: str, threshold: float) -> Dict:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return self._get_llm_response(
            model, message, "gemini-1.5-flash", threshold, message
        )

    async def _huggingface_provider(self, message: str, threshold: float) -> Dict:
        client = InferenceClient(token=settings.hf_token)
        return self._get_llm_response(
            client, message, "meta-llama/Llama-3.1-8B-Instruct", threshold, message
        )

    async def _mistral_provider(self, message: str, threshold: float) -> Dict:
        client = Mistral(api_key=settings.mistral_api_key)
        return self._get_llm_response(
            client, message, "mistral-small-latest", threshold, message
        )

    def _get_llm_response(
        self, client, message: str, model: str, threshold: float, new_message: str
    ) -> Dict:
        prompt = self._build_prompt(message)

        if isinstance(client, Groq):
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )
            content = response.choices[0].message.content
        elif isinstance(client, genai.GenerativeModel):
            response = client.generate_content(prompt)
            content = response.text
        elif isinstance(client, InferenceClient):
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )
            content = response.choices[0].message.content
        elif isinstance(client, Mistral):
            response = client.chat(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )
            content = response.choices[0].message.content
        else:
            raise Exception("Unknown LLM client type.")

        return self._parse_llm_output(content, new_message, model, threshold)

    def _build_prompt(self, message: str) -> str:
        return f"""
        Analyze the following conversation for PII (Personally Identifiable Information) based on a Singaporean context.
        The user's message is the first in the string, and the rest are the past 20 messages in the conversation.
        Be extra vigilant for common shorthands and abbreviations, such as 'blk' for 'Block', 'Rd' for 'Road', and incomplete addresses.
        The PII types to detect are: EMAIL_ADDRESS, PHONE_NUMBER, ADDRESS, POSTAL_CODE, UNIT_NUMBER, SG_NRIC.
        If an address is mentioned, even if incomplete, it should be flagged.

        Respond with a JSON object with the following structure:
        {{
            "has_pii": boolean,
            "detected_types": ["type1", "type2", ...],
            "confidence": float (0.0 to 1.0),
            "filtered_message": "The message with PII replaced by placeholders like [EMAIL_ADDRESS]",
            "reasoning": "Your reasoning for the detection."
        }}

        Message: "{message}"
        """

    def _parse_llm_output(
        self, content: str, original_message: str, provider: str, threshold: float
    ) -> Dict:
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            data = json.loads(content)
            pii_detection = PIIDetection(
                has_pii=data.get("has_pii", False),
                detected_types=data.get("detected_types", []),
                confidence=data.get("confidence", 0.0),
                filtered_message=data.get("filtered_message", original_message),
                reasoning=data.get("reasoning", ""),
                provider=provider,
            )

            if pii_detection.has_pii and pii_detection.confidence >= threshold:
                return {
                    "filtered": True,
                    "content": pii_detection.filtered_message,
                    "detected": pii_detection.detected_types,
                    "confidence": pii_detection.confidence,
                    "reasoning": pii_detection.reasoning,
                    "provider": pii_detection.provider,
                }
            else:
                return {
                    "filtered": False,
                    "content": original_message,
                    "detected": [],
                    "confidence": 0.0,
                    "reasoning": "No PII detected or confidence below threshold.",
                    "provider": provider,
                }
        except (json.JSONDecodeError, KeyError):
            return {
                "filtered": False,
                "content": original_message,
                "detected": [],
                "confidence": 0.0,
                "reasoning": "Failed to parse LLM output.",
                "provider": provider,
            }


content_filter_service = ContentFilterService()

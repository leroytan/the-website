import re
import json
import logging
import csv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum

class PIIDetection(BaseModel):
    has_pii: bool
    detected_types: List[str]
    confidence: float
    filtered_message: str
    reasoning: str
    provider: str

class ContentFilterService:
    """
    Lightweight regex-based content filtering service for detecting PII in chat messages.
    Optimized for low resource usage on 0.5 CPU instances.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContentFilterService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_patterns()
            ContentFilterService._initialized = True
    
    def _load_singapore_roads(self) -> List[str]:
        """Load Singapore road names from CSV file"""
        roads = []
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'road_names.csv')
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    if row and row[0].strip():  # Check if row exists and has content
                        roads.append(row[0].strip())
            logging.info(f"Loaded {len(roads)} Singapore road names from CSV")
        except FileNotFoundError:
            logging.warning(f"Road names CSV file not found at {csv_path}, using fallback list")
            # Fallback to a minimal list if CSV is not found
            roads = [
                "ORCHARD ROAD", "MARINA BAY", "MARINA BAY SANDS", "RAFFLES PLACE", "CLARKE QUAY", "BOAT QUAY",
                "CHINATOWN", "LITTLE INDIA", "KAMPONG GLAM", "BUGIS STREET", "ARAB STREET", "MARINA BOULEVARD",
                "MARINA GARDENS DRIVE", "MARINA PLACE", "MARINA VIEW", "MARINA WAY"
            ]
        except Exception as e:
            logging.error(f"Error loading road names from CSV: {e}, using fallback list")
            roads = [
                "ORCHARD ROAD", "MARINA BAY", "MARINA BAY SANDS", "RAFFLES PLACE", "CLARKE QUAY", "BOAT QUAY",
                "CHINATOWN", "LITTLE INDIA", "KAMPONG GLAM", "BUGIS STREET", "ARAB STREET", "MARINA BOULEVARD",
                "MARINA GARDENS DRIVE", "MARINA PLACE", "MARINA VIEW", "MARINA WAY"
            ]
        
        return roads

    def _initialize_patterns(self):
        """Initialize regex patterns for PII detection"""
        
        # Load Singapore road names from CSV file
        singapore_roads = self._load_singapore_roads()
        
        # Singapore area names
        singapore_areas = [
            "Ang Mo Kio", "Bedok North", "Bedok South", "Bishan", "Bukit Batok", "Bukit Merah",
            "Bukit Panjang", "Bukit Timah", "Central Area", "Changi", "Changi Bay", "Choa Chu Kang",
            "Clementi", "Geylang", "Hougang", "Jurong East", "Jurong West", "Kallang", "Lim Chu Kang",
            "Mandai", "Marine Parade", "Newton", "Novena", "Orchard", "Outram", "Pasir Ris",
            "Paya Lebar", "Pioneer", "Punggol", "Queenstown", "River Valley", "Rochor", "Seletar",
            "Sembawang", "Sengkang", "Serangoon", "Simpang", "Southern Islands", "Straits View",
            "Sungei Kadut", "Tampines", "Tanglin", "Tengah", "Thomson", "Toa Payoh", "Tuas",
            "Western Islands", "Western Water Catchment", "Woodlands", "Yishun", "Boon Lay",
            "Ghim Moh", "Gul", "Kent Ridge", "Nanyang", "Pasir Laba", "Teban Gardens", "Toh Tuck",
            "Tuas South", "West Coast"
        ]
        
        # Create regex patterns
        road_pattern = "|".join(re.escape(road) for road in singapore_roads)
        area_pattern = "|".join(re.escape(area) for area in singapore_areas)
        
        self.patterns = {
            # Email addresses
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE),
            
            # Singapore phone numbers
            "sg_phone_strict": re.compile(r'\b[689]\d{7}\b'),  # 8 digits starting with 6, 8, or 9
            "sg_phone_intl": re.compile(r'\+65[-.\s]?[689]\d{7}\b'),  # International format
            "sg_phone_formatted": re.compile(r'\b\d{4}[-.\s]\d{4}\b'),  # 4-4 format
            
            # Addresses with postal codes (6 digits)
            "postal_code": re.compile(r'\b\d{6}\b'),
            
            # HDB/Block addresses
            "hdb_block": re.compile(rf'\b(?:Block|Blk)\s+\d+[A-Za-z]?\s+(?:{area_pattern}|[A-Za-z\s]+(?:Estate|Park|Gardens?|Heights?|View|Place|Court|Square|North|South|East|West|Central))\b', re.IGNORECASE),
            
            # Street addresses with road names
            "street_address": re.compile(rf'\b\d+[A-Za-z]?\s+(?:{road_pattern})\b', re.IGNORECASE),
            
            # Unit numbers
            "unit_number": re.compile(r'#\d{2}-\d{2,3}|(?:unit|Unit)\s*[#]?\d{1,2}[-\s]?\d{1,3}\b|\b\d{1,3}-\d{1,3}\b', re.IGNORECASE),
            
            # Singapore area names (standalone)
            "sg_area": re.compile(rf'\b(?:{area_pattern})\b', re.IGNORECASE),
            
            # NRIC/FIN (strict)
            "nric": re.compile(r'\b[STFGstfg]\d{7}[A-Za-z]\b'),
        }
        
        # Price/payment exclusion patterns
        self.price_exclusions = re.compile(r'(?:\$|SGD|dollars?|cents?|price|cost|pay|paid|fee|charge|bill|rent|salary|wage|income|budget|total|amount)\s*\d+|\d+\s*(?:\$|SGD|dollars?|cents?)', re.IGNORECASE)
        
        # Context words that indicate non-PII usage
        self.deny_context = {
            "cost", "costs", "paid", "pay", "price", "expensive", "cheap", "buy", "bought", "sell", "sold",
            "worth", "dollars", "total", "amount", "fee", "charge", "bill", "payment", "rent", "salary",
            "wage", "income", "profit", "loss", "budget", "error", "room", "chapter", "shares",
            "traded", "score", "ratio", "temperature", "degrees", "range", "between", "tasks", "pages",
            "restaurant", "business", "lunch", "dinner", "meal", "food", "menu", "order", "booking"
        }
    
    def _has_price_context(self, message: str) -> bool:
        """Check if message contains price/payment context"""
        return bool(self.price_exclusions.search(message))
    
    def _has_deny_context(self, message: str, window_size: int = 50) -> bool:
        """Check if message contains context words that suggest non-PII usage"""
        words = set(re.findall(r'\b\w+\b', message.lower()))
        return len(words & self.deny_context) > 0
    
    def _extract_context_around_match(self, message: str, match_start: int, match_end: int, window: int = 30) -> str:
        """Extract context around a regex match"""
        start = max(0, match_start - window)
        end = min(len(message), match_end + window)
        return message[start:end].lower()
    
    def _filter_phone_numbers(self, message: str) -> List[Dict]:
        """Filter phone numbers with context awareness"""
        detected = []
        
        # Check for price context first
        has_price_context = self._has_price_context(message)
        
        # Check strict Singapore phone patterns
        for pattern_name in ["sg_phone_strict", "sg_phone_intl", "sg_phone_formatted"]:
            pattern = self.patterns[pattern_name]
            for match in pattern.finditer(message):
                context = self._extract_context_around_match(message, match.start(), match.end())
                
                # Skip if it's clearly a price (up to $200 as requested)
                if has_price_context:
                    # Extract the number to check if it's under $200
                    number_str = re.sub(r'[^\d]', '', match.group())
                    if number_str.isdigit():
                        number = int(number_str)
                        if number <= 200 and any(word in context for word in ["$", "sgd", "dollar", "price", "cost", "pay"]):
                            continue
                
                # Skip if deny context without phone indicators
                if self._has_deny_context(context) and not any(word in context for word in ["call", "phone", "contact", "whatsapp", "text"]):
                    continue
                
                detected.append({
                    "type": "PHONE_NUMBER",
                    "match": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.9 if pattern_name == "sg_phone_intl" else 0.8
                })
                # Remove break to allow multiple phone numbers to be detected
        
        return detected
    
    def _filter_addresses(self, message: str) -> List[Dict]:
        """Filter addresses with context awareness"""
        detected = []
        
        # Check for HDB/Block addresses
        for match in self.patterns["hdb_block"].finditer(message):
            detected.append({
                "type": "ADDRESS",
                "match": match.group(),
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.95
            })
        
        # Check for street addresses
        for match in self.patterns["street_address"].finditer(message):
            detected.append({
                "type": "ADDRESS",
                "match": match.group(),
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.9
            })
        
        # Check for postal codes with more specific context checking
        for match in self.patterns["postal_code"].finditer(message):
            context = self._extract_context_around_match(message, match.start(), match.end())
            
            # More specific price context check - only skip if directly related to price
            is_direct_price = any(word in context for word in ["$", "sgd", "dollar", "price", "cost", "pay", "paid"])
            
            # More specific deny context check - exclude postal code specific words
            postal_deny_context = self.deny_context - {"code", "room", "chapter"}
            has_deny_context = len(set(re.findall(r'\b\w+\b', context.lower())) & postal_deny_context) > 0
            
            if not is_direct_price and not has_deny_context:
                detected.append({
                    "type": "POSTAL_CODE",
                    "match": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.8
                })
        
        # Check for unit numbers
        for match in self.patterns["unit_number"].finditer(message):
            # For unit numbers, we should ignore the broad price context and check more specific context.
            context = self._extract_context_around_match(message, match.start(), match.end())
            
            # More specific check to avoid being filtered by generic price words
            is_price_context = any(word in context for word in ["price", "cost", "buy", "sell", "dollar", "sgd"])
            has_address_context = any(word in context for word in ["unit", "apartment", "flat", "block", "address", "live", "stay", "#"])
            
            # Check if it's a standalone unit number pattern (like "01-02")
            is_unit_pattern = re.match(r'^\d{2}-\d{2}$', match.group().strip())
            
            # Check for sports/academic context that should be excluded
            has_sports_context = any(word in context for word in ["score", "match", "game", "vs", "against"])
            has_academic_context = any(word in context for word in ["chapter", "section", "page", "lesson"])
            
            # Allow standalone unit patterns or those with address context, but not price/sports/academic context
            if (has_address_context or is_unit_pattern) and not is_price_context and not has_sports_context and not has_academic_context:
                detected.append({
                    "type": "UNIT_NUMBER",
                    "match": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.85 # Increased confidence due to better context checking
                })
        
        return detected
    
    def _filter_emails(self, message: str) -> List[Dict]:
        """Filter email addresses"""
        detected = []
        for match in self.patterns["email"].finditer(message):
            detected.append({
                "type": "EMAIL_ADDRESS",
                "match": match.group(),
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.95
            })
        return detected
    
    def _filter_nric(self, message: str) -> List[Dict]:
        """Filter NRIC/FIN numbers"""
        detected = []
        for match in self.patterns["nric"].finditer(message):
            detected.append({
                "type": "SG_NRIC",
                "match": match.group(),
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.9
            })
        return detected
    
    def _anonymize_message(self, message: str, detections: List[Dict]) -> str:
        """Replace detected PII with placeholders"""
        # Sort detections by start position in reverse order to avoid index shifting
        sorted_detections = sorted(detections, key=lambda x: x["start"], reverse=True)
        
        anonymized = message
        for detection in sorted_detections:
            placeholder = f"[{detection['type']}]"
            anonymized = anonymized[:detection["start"]] + placeholder + anonymized[detection["end"]:]
        
        return anonymized
    
    async def filter_message(self, message: str, threshold: float = 0.7) -> Dict:
        """
        Main filtering function with regex-based PII detection.
        
        Args:
            message: The message to filter
            threshold: Confidence threshold for blocking (default: 0.7)
            
        Returns:
            Dict with filtering results
        """
        all_detections = []
        
        # Run all detection filters
        all_detections.extend(self._filter_emails(message))
        all_detections.extend(self._filter_phone_numbers(message))
        all_detections.extend(self._filter_addresses(message))
        all_detections.extend(self._filter_nric(message))
        
        # Remove duplicates and overlapping detections
        unique_detections = []
        for detection in sorted(all_detections, key=lambda x: (x["start"], -x["confidence"])):
            # Check for overlap with existing detections
            overlaps = False
            for existing in unique_detections:
                if (detection["start"] < existing["end"] and detection["end"] > existing["start"]):
                    overlaps = True
                    break
            if not overlaps:
                unique_detections.append(detection)
        
        # Filter by confidence threshold
        high_confidence_detections = [d for d in unique_detections if d["confidence"] >= threshold]
        
        if high_confidence_detections:
            # Create anonymized message
            anonymized_message = self._anonymize_message(message, high_confidence_detections)
            detected_types = list(set(d["type"] for d in high_confidence_detections))
            avg_confidence = sum(d["confidence"] for d in high_confidence_detections) / len(high_confidence_detections)
            
            return {
                "filtered": True,
                "content": anonymized_message,
                "detected": detected_types,
                "confidence": avg_confidence,
                "reasoning": f"Detected {len(high_confidence_detections)} PII pattern(s): {', '.join(detected_types)}",
                "provider": "regex_filter"
            }
        else:
            return {
                "filtered": False,
                "content": message,
                "detected": [],
                "confidence": 0.0,
                "reasoning": "No PII patterns detected above threshold",
                "provider": "regex_filter"
            }

# Singleton instance
content_filter_service = ContentFilterService()
# -*- coding: utf-8 -*-
import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

###############################################################################
# 1) Normalization
###############################################################################

ZERO_WIDTH = re.compile(r"[\u200B-\u200D\uFEFF]")  # zero-width chars
OBFUSCATED_AT = re.compile(r"(?i)(?:\(|\[)?\s*at\s*(?:\)|\])?")
OBFUSCATED_DOT = re.compile(r"(?i)\s*(?:dot|•|·|\[dot\]|\(dot\)|\.)\s*")
MULTISPACE = re.compile(r"\s{2,}")


def normalize_text(text: str) -> str:
    # Normalize Unicode, case-fold, and smooth common evasions.
    t = unicodedata.normalize("NFKC", text).lower()
    t = ZERO_WIDTH.sub(" ", t)  # Replace with space instead of empty string
    t = OBFUSCATED_AT.sub("@", t)
    t = OBFUSCATED_DOT.sub(".", t)
    t = MULTISPACE.sub(" ", t).strip()
    # Handle accented characters
    t = t.replace("é", "e").replace("è", "e").replace("ê", "e")
    t = t.replace("á", "a").replace("à", "a").replace("â", "a")
    t = t.replace("í", "i").replace("ì", "i").replace("î", "i")
    t = t.replace("ó", "o").replace("ò", "o").replace("ô", "o")
    t = t.replace("ú", "u").replace("ù", "u").replace("û", "u")
    t = t.replace("ñ", "n").replace("ç", "c")
    # Clean up extra spaces around @
    t = re.sub(r"\s+@\s+", "@", t)
    return t


###############################################################################
# 2) Primitive validators (email first, since you already block it)
###############################################################################

EMAIL_RE = re.compile(
    r"""
    (?xi)
    \b
    [a-z0-9._%+-]{1,64}
    @
    (?:[a-z0-9-]+\.)+[a-z]{2,}
    \b
""",
    re.VERBOSE | re.IGNORECASE,
)

# Optional: quick phone pattern (kept here for completeness)
PHONE_RE = re.compile(r"(?x)\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?){2,4}\d\b")

###############################################################################
# 3) High-coverage social URL detector (easy wins)
###############################################################################

SOCIAL_DOMAINS = (
    r"instagram\.com|t\.me|telegram\.me|wa\.me|whatsapp\.com|web\.whatsapp\.com|"
    r"twitter\.com|x\.com|facebook\.com|m\.facebook\.com|fb\.com|messenger\.com|"
    r"threads\.net|tiktok\.com|snapchat\.com|discord\.gg|discord\.com|"
    r"linkedin\.com|reddit\.com|pinterest\.com|tumblr\.com|"
    r"weixin\.qq\.com|wechat\.com|line\.me|kakao(?:talk)?\.com|viber\.com|"
    r"vk\.com|ok\.ru|youtube\.com|twitch\.tv|onlyfans\.com|patreon\.com|"
    r"lemon8-app\.com"
)

SOCIAL_URL_RE = re.compile(
    rf'\bhttps?://(?:www\.)?(?:{SOCIAL_DOMAINS})/[^\s<>"\'\)]{{1,128}}', re.IGNORECASE
)

###############################################################################
# 4) Generic @handle detector (works for IG, TT, X, Threads, Telegram, Discord)
###############################################################################

AT_HANDLE_RE = re.compile(
    r"""
    (?xi)
    (?<![\w@])                # not part of a larger token
    @
    (
      [a-z0-9]                # start alnum
      [a-z0-9._-]{0,30}       # body
      [a-z0-9]                # end alnum
    )
    (?![\w.])                 # avoid trailing domain-like continuations
""",
    re.VERBOSE | re.IGNORECASE,
)

###############################################################################
# 5) Platform-cued bare-handle detector (no '@', near a platform cue)
###############################################################################

PLATFORM_CUES = re.compile(
    r"""
    (?xi)
    \b(
      insta|instagram|tt|tiktok|threads|
      twitter|x|snap|snapchat|fb|facebook|messenger|
      wa|whatsapp|tele|telegram|tg|discord|
      line|wechat|weixin|kakao|viber|
      pinterest|tumblr|reddit|linkedin|
      yt|youtube|twitch|vk|ok|lemon8
    )\b
""",
    re.VERBOSE | re.IGNORECASE,
)

HANDLE_TOKEN_RE = re.compile(
    r"""
    (?xi)
    (?<!\w)
    [a-z][a-z0-9._-]{1,30}[a-z0-9]
    (?!\w)
""",
    re.VERBOSE | re.IGNORECASE,
)

# Discord legacy discriminator (name#1234)
DISCORD_TAG_RE = re.compile(
    r"""
    (?xi)
    (?<!\w)
    [a-z0-9][a-z0-9._-]{1,30}[a-z0-9]\s?#\s?\d{4}
    (?!\w)
""",
    re.VERBOSE | re.IGNORECASE,
)

# Optional platform-constrained validators when a cue is present
PLATFORM_SPECIFIC = {
    "telegram": re.compile(r"(?i)^[a-z]\w{4,31}$"),
    "snapchat": re.compile(r"(?i)^[a-z][a-z0-9_-]{2,14}$"),
    "wechat": re.compile(r"(?i)^[a-z][a-z0-9_-]{5,19}$"),
}

###############################################################################
# 6) Context triggers to boost confidence
###############################################################################

CONTEXT_TRIGGERS_RE = re.compile(
    r"""
    (?xi)
    \b(
      add\s+me\s+(?:on|at|via)|
      dm\s+me|
      my\s+(?:id|handle|user(?:name)?)\s+is|
      reach\s+me\s+on|
      follow\s+me|
      contact\s+me\s+on|
      hit\s+me\s+up|
      chat\s+me\s+on
    )\b
""",
    re.VERBOSE | re.IGNORECASE,
)

###############################################################################
# 7) Public API
###############################################################################


@dataclass
class MatchEvidence:
    kind: str  # 'url' | 'at' | 'bare' | 'discord' | 'trigger' | 'platform_cue'
    span: Tuple[int, int]
    value: str


@dataclass
class DetectionResult:
    blocked: bool
    score: int
    evidence: List[MatchEvidence]


def _window(text: str, start: int, end: int, radius_chars: int = 80) -> str:
    a = max(0, start - radius_chars)
    b = min(len(text), end + radius_chars)
    return text[a:b]


def extract_social_shares(
    text: str,
    whitelist: Optional[Iterable[str]] = None,
    use_phone_guard: bool = False,
    debug: bool = False,
) -> DetectionResult:
    """
    Analyze `text` and return a DetectionResult with scoring + evidence.
    `whitelist`: in-app mentions to ignore (e.g., {'@mods', '@support'})
    `use_phone_guard`: if True, lowers score when line looks like code/log/phone noise
    """
    whitelist = {w.lower() for w in (whitelist or set())}
    t = normalize_text(text)

    score = 0
    evidence: List[MatchEvidence] = []

    # Guard rails: short-circuit or reduce false positives
    if EMAIL_RE.search(t):
        return DetectionResult(
            False, 0, evidence
        )  # your email filter handles this first

    # 1) Social URLs
    for m in SOCIAL_URL_RE.finditer(t):
        evidence.append(MatchEvidence("url", m.span(), m.group(0)))
    if evidence and any(e.kind == "url" for e in evidence):
        score += 2

    # 2) @handles (skip whitelisted)
    for m in AT_HANDLE_RE.finditer(t):
        handle = f"@{m.group(1)}"
        if handle in whitelist:
            continue
        evidence.append(MatchEvidence("at", m.span(), handle))
    if any(e.kind == "at" for e in evidence):
        score += 2

    # 3) Platform cues and local windows for bare handles / discord tags
    for cue in PLATFORM_CUES.finditer(t):
        evidence.append(MatchEvidence("platform_cue", cue.span(), cue.group(1)))
        win = _window(t, *cue.span(), radius_chars=120)

        # Discord discriminator near a cue
        for m in DISCORD_TAG_RE.finditer(win):
            evidence.append(
                MatchEvidence("discord", (cue.start(), cue.end()), m.group(0))
            )
            score += 1

        # Bare handle near a cue
        for m in HANDLE_TOKEN_RE.finditer(win):
            token = m.group(0)
            # Skip if token is part of the URL or already counted
            if any(token in e.value for e in evidence if e.kind in ["url", "at"]):
                continue
            # If we can attribute to a specific platform, optionally validate
            platform = cue.group(1)
            validator = None
            if "tele" in platform or platform in {"tg", "telegram"}:
                validator = PLATFORM_SPECIFIC["telegram"]
            elif platform in {"snap", "snapchat"}:
                validator = PLATFORM_SPECIFIC["snapchat"]
            elif platform in {"wechat", "weixin"}:
                validator = PLATFORM_SPECIFIC["wechat"]

            if validator is None or validator.match(token):
                evidence.append(MatchEvidence("bare", (cue.start(), cue.end()), token))
                score += 1  # base increment; validators keep false positives low

    # 4) General context triggers anywhere
    if CONTEXT_TRIGGERS_RE.search(t):
        evidence.append(
            MatchEvidence("trigger", CONTEXT_TRIGGERS_RE.search(t).span(), "context")
        )
        score += 1

    # 5) Optional de-noising for code/loggy lines or phone-like strings
    if use_phone_guard:
        if any(
            kw in t for kw in (" def ", ";", "{", "}", " exception ", " stacktrace ")
        ):
            score = max(0, score - 1)
        if PHONE_RE.search(t) and score < 2:
            score = max(0, score - 1)

    blocked = score >= 2
    return DetectionResult(blocked, score, evidence)


def is_social_share(
    text: str, whitelist: Optional[Iterable[str]] = None, use_phone_guard: bool = False
) -> bool:
    """Boolean convenience wrapper."""
    return extract_social_shares(text, whitelist, use_phone_guard).blocked

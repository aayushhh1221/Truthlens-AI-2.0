"""
TruthLens AI 2.0 — Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── API Keys ────────────────────────────────────────────────
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")
GOOGLE_API_KEY     = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID      = os.getenv("GOOGLE_CSE_ID", "")
HF_TOKEN           = os.getenv("HF_TOKEN", "")

# ─── App Meta ────────────────────────────────────────────────
APP_NAME           = "TruthLens AI"
APP_VERSION        = "2.0.0"
APP_TAGLINE        = "Multi-Agent Misinformation & Deepfake Detection"

# ─── Gemini ──────────────────────────────────────────────────
GEMINI_MODEL       = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ─── Thresholds ──────────────────────────────────────────────
THRESHOLD_HIGH_RISK   = 70
THRESHOLD_MEDIUM_RISK = 40

# ─── File Support ────────────────────────────────────────────
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
SUPPORTED_DOC_TYPES   = ["pdf", "png", "jpg", "jpeg"]

# ─── Database ────────────────────────────────────────────────
DATABASE_PATH = os.getenv("DATABASE_PATH", "truthlens.db")

# ─── Forensics ───────────────────────────────────────────────
ELA_QUALITY   = 90      # JPEG quality for ELA
ELA_SCALE     = 20      # Amplification scale for ELA diff

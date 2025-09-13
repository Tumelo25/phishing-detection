"""
Centralized API keys and endpoints for external integrations.
Populate values via .env or manual assignment.
"""

import os
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, "config", ".env"))

# ==========================
# HIBP (Have I Been Pwned)
# ==========================
HIBP_API_KEY = os.getenv("HIBP_API_KEY")  # Paid tier required
HIBP_BREACH_API = "https://haveibeenpwned.com/api/v3/breachedaccount/"
PWNED_PASS_API = "https://api.pwnedpasswords.com/range/"  # free, no key

# ==========================
# VirusTotal
# ==========================
VT_API_KEY = os.getenv("VT_API_KEY")  # Free tier available
VT_URL_API = "https://www.virustotal.com/api/v3/urls"
VT_DOMAIN_API = "https://www.virustotal.com/api/v3/domains/"

# ==========================
# PhishTank
# ==========================
PHISHTANK_API_KEY = os.getenv("PHISHTANK_API_KEY")  # Optional
PHISHTANK_API = "https://phishtank.org/api/"

# ==========================
# AbuseIPDB (optional)
# ==========================
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
ABUSEIPDB_API = "https://api.abuseipdb.com/api/v2/check"

# ==========================
# Convenience dict (optional)
# ==========================
ALL_KEYS = {
    "HIBP_API_KEY": HIBP_API_KEY,
    "VT_API_KEY": VT_API_KEY,
    "PHISHTANK_API_KEY": PHISHTANK_API_KEY,
    "ABUSEIPDB_API_KEY": ABUSEIPDB_API_KEY,
}
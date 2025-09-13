import os, sys, hashlib, requests, time
from typing import Optional, Dict

# Ensure project root on path for config import
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from config import settings

PWNED_PASS_API = "https://api.pwnedpasswords.com/range/"         # no key needed
HIBP_BREACH_API = "https://haveibeenpwned.com/api/v3/breachedaccount/"  # needs key

def check_password_pwned(password: str) -> int:
    """
    Returns the number of times this password appears in known breaches.
    Uses k-anonymity (no API key required).
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = PWNED_PASS_API + prefix
    resp = requests.get(url, timeout=10, headers={"Add-Padding": "true"})
    resp.raise_for_status()
    count = 0
    for line in resp.text.splitlines():
        hash_suffix, hits = line.split(":")
        if hash_suffix.strip() == suffix:
            count = int(hits.strip())
            break
    return count

def check_email_breaches(email: str) -> Optional[int]:
    """
    Returns the number of breaches for an email using HIBP (requires API key).
    If no key present, returns None (graceful skip).
    """
    api_key = settings.HIBP_API_KEY
    if not api_key:
        return None
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "phishing-detection-research/1.0",
    }
    params = {"truncateResponse": "true"}
    # HIBP rate limit: be polite; if you batch in future, sleep between calls.
    r = requests.get(HIBP_BREACH_API + email, headers=headers, params=params, timeout=15)
    if r.status_code == 404:
        # 404 == no breach for that account (per HIBP docs)
        return 0
    r.raise_for_status()
    breaches = r.json()  # list of breach summaries
    return len(breaches) if isinstance(breaches, list) else 0

def darkweb_risk(email: Optional[str] = None, password: Optional[str] = None) -> Dict:
    """
    Combines password and (optional) email breach checks into a simple risk verdict.
    Returns: dict with risk_score, verdict, reasons, evidence.
    """
    score = 0
    reasons = []
    evidence = {}

    # Password exposure
    pw_hits = None
    if password:
        try:
            pw_hits = check_password_pwned(password)
            evidence["password_hits"] = pw_hits
            if pw_hits and pw_hits > 0:
                score += 2 if pw_hits > 1000 else 1
                reasons.append(f"Password found in {pw_hits} breaches")
        except Exception as e:
            evidence["password_error"] = str(e)

    # Email breaches (optional, requires key)
    email_breaches = None
    if email:
        try:
            email_breaches = check_email_breaches(email)
            evidence["email_breaches"] = email_breaches
            if email_breaches is None:
                reasons.append("Email breach check skipped (no HIBP API key)")
            elif email_breaches > 0:
                score += 1 if email_breaches <= 3 else 2
                reasons.append(f"Email appears in {email_breaches} breaches")
        except Exception as e:
            evidence["email_error"] = str(e)

    verdict = "Safe"
    if score == 1:
        verdict = "Elevated"
    elif score >= 2:
        verdict = "High Risk"

    return {
        "risk_score": score,
        "verdict": verdict,
        "reasons": reasons,
        "evidence": evidence,
    }

if __name__ == "__main__":
    # Quick smoke tests (you can change inputs)
    print(darkweb_risk(email=None, password="Password123"))

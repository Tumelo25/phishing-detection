import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from detection_engine.darkweb_intel import darkweb_risk

if __name__ == "__main__":
    # Simple CLI usage:
    # python detection_engine\predict_darkweb.py <email-or-"-"> <password-or-"-">
    email = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else None
    password = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None

    result = darkweb_risk(email=email, password=password)
    print("Verdict:", result["verdict"])
    print("Reasons:", result["reasons"])
    print("Evidence:", result["evidence"])

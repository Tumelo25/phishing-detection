import os, sys
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from detection_engine.network_analysis import analyze_url, risk_score

def classify_url(url: str):
    result = analyze_url(url)
    verdict = risk_score(result)
    return {**result, **verdict}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict_network.py <url>")
    else:
        url = sys.argv[1]
        result = classify_url(url)
        print(f"🔗 URL: {result['domain']}")
        print(f"Verdict: {result['verdict']}")
        print(f"Reasons: {result['reasons']}")

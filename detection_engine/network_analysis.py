import socket, ssl, whois, requests
from datetime import datetime

def check_domain_age(domain):
    try:
        w = whois.whois(domain)
        if w.creation_date:
            # Some domains return a list of dates
            created = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
            age_days = (datetime.now() - created).days
            return age_days
    except Exception:
        return None
    return None

def check_ssl(domain):
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                exp = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_left = (exp - datetime.now()).days
                return days_left
    except Exception:
        return None

def check_dns(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def analyze_url(url):
    from urllib.parse import urlparse
    domain = urlparse(url).netloc

    result = {
        "domain": domain,
        "domain_age_days": check_domain_age(domain),
        "ssl_days_left": check_ssl(domain),
        "dns_resolves": check_dns(domain),
    }
    return result

if __name__ == "__main__":
    test_url = "https://example.com"
    print(analyze_url(test_url))

def risk_score(result):
    score = 0
    reasons = []

    if result["domain_age_days"] is None or result["domain_age_days"] < 30:
        score += 1
        reasons.append("Domain is too new")

    if result["ssl_days_left"] is None or result["ssl_days_left"] < 15:
        score += 1
        reasons.append("SSL certificate issue")

    if not result["dns_resolves"]:
        score += 1
        reasons.append("Domain does not resolve")

    if score == 0:
        verdict = "Safe"
    elif score == 1:
        verdict = "Suspicious"
    else:
        verdict = "High Risk"

    return {"risk_score": score, "verdict": verdict, "reasons": reasons}


if __name__ == "__main__":
    test_url = "https://example.com"
    result = analyze_url(test_url)
    print(result)
    print(risk_score(result))

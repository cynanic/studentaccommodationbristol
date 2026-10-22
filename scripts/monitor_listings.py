#!/usr/bin/env python3
"""Source health checks only; never infer prices or availability from HTTP status."""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DATA = Path("data/properties.json")
OUTPUT = Path("reports/listings-monitor.json")
STALE_DAYS = 7

def inspect(row, today):
    url = row["source"]
    request = Request(url, headers={"User-Agent": "StudentAccommodationBristolListingMonitor/1.0 (source health check)"})
    status = "unknown"
    http_code = None
    try:
        with urlopen(request, timeout=12) as response:
            http_code = response.status
            status = "reachable" if 200 <= http_code < 400 else "http_error"
    except HTTPError as exc:
        http_code = exc.code
        status = "blocked_or_missing" if exc.code in (403, 404, 429) else "http_error"
    except (URLError, TimeoutError, OSError):
        status = "connection_error"
    checked = datetime.fromisoformat(row["checked"]).date()
    age = (today - checked).days
    return {
        "name": row["name"],
        "provider": row["provider"],
        "source_url": url,
        "source_health": status,
        "http_status": http_code,
        "listing_last_verified": row["checked"],
        "listing_age_days": age,
        "review_required": age > STALE_DAYS or status != "reachable",
        "note": "HTTP health does not verify prices, offers, booking status or academic year."
    }

def main():
    rows = json.loads(DATA.read_text(encoding="utf-8"))
    today = datetime.now(timezone.utc).date()
    checks = []
    for row in rows:
        checks.append(inspect(row, today))
        time.sleep(0.3)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Do not include run timestamps: avoid meaningless daily PR churn.
    OUTPUT.write_text(json.dumps({"schema_version": 1, "checks": checks}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Checked {len(checks)} sources; {sum(c['review_required'] for c in checks)} require review.")

if __name__ == "__main__":
    main()

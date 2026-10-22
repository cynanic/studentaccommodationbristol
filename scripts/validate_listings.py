#!/usr/bin/env python3
"""Validate current listing records without altering the published dataset."""
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

DATA = Path("data/properties.json")
REQUIRED = ("name", "provider", "source", "checked", "room_types")
def validate(rows):
    errors = []
    names = set()
    if not isinstance(rows, list):
        return ["Expected a JSON array"]
    for i, row in enumerate(rows):
        tag = f"listing {i + 1}"
        if not isinstance(row, dict):
            errors.append(f"{tag}: expected object")
            continue
        for field in REQUIRED:
            if not row.get(field):
                errors.append(f"{tag}: missing {field}")
        name = str(row.get("name", "")).casefold().strip()
        if name in names:
            errors.append(f"{tag}: duplicate name {name}")
        names.add(name)
        if row.get("from_price") is not None:
            price = row["from_price"]
            if isinstance(price, bool) or not isinstance(price, (int, float)) or not 0 < price < 2000:
                errors.append(f"{tag}: implausible from_price")
        try:
            if date.fromisoformat(row["checked"]) > date.today():
                errors.append(f"{tag}: checked date is in the future")
        except (ValueError, KeyError, TypeError):
            errors.append(f"{tag}: invalid checked date")
        if urlparse(str(row.get("source", ""))).scheme != "https":
            errors.append(f"{tag}: source must be HTTPS")
        if "academic_year" in row and row["academic_year"] is not None:
            if not __import__("re").fullmatch(r"20\d\d/\d\d", str(row["academic_year"])):
                errors.append(f"{tag}: invalid academic_year")
    return errors

if __name__ == "__main__":
    errors = validate(json.loads(DATA.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("\n".join(errors))
    print("Listings structure validated; historical prices have not been independently verified.")

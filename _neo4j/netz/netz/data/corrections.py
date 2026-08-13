"""Small, explicit, report-only corrections applied before country partitioning."""
import json
from pathlib import Path


def load_country_overrides(path: str) -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("scope") != "latex_only":
        raise RuntimeError("country overrides must declare scope=latex_only")
    result = {}
    for eid, row in data.get("overrides", {}).items():
        country = row.get("country")
        if not isinstance(country, str) or len(country) != 2:
            raise RuntimeError(f"invalid country override for {eid}: {country!r}")
        result[eid] = country.upper()
    return result

import re
from pathlib import Path
from typing import Any



ROOT = Path(__file__).resolve().parents[1]


def load_rules() -> dict[str, Any]:
    # Keep the runtime dependency-free. This reads the canonical YAML list
    # without introducing a second rule source or requiring PyYAML in deploys.
    text = (ROOT / "config/qualification_rules.yaml").read_text()
    line = next(x for x in text.splitlines() if x.startswith("required_for_preliminary_review:"))
    fields = re.findall(r"[a-z_]+", line.split(":", 1)[1])
    return {"required_for_preliminary_review": fields}


def extract_values(text: str, requested_field: str | None = None) -> dict[str, Any]:
    """Small deterministic extractor; an LLM can replace this behind the same contract."""
    t = text.casefold()
    out: dict[str, Any] = {}
    name = re.search(r"\bmy name is\s+([A-Za-z]+(?:\s+[A-Za-z]+){1,3}?)(?=\s+and\b|\.|,|$)", text, re.I)
    if name:
        out["full_name"] = " ".join(name.group(1).split()).strip(" .,")
    business = re.search(r"\b(?:run|own|operate)\s+(?:(?:a|an|the)\s+)?(?:small\s+)?([A-Za-z]+)\s+(?:shop|business)", t)
    if business:
        out["business_type"] = business.group(1)
    company = re.search(r"\b(?:my company is|business is|called)\s+([A-Za-z][A-Za-z ]{1,40}?)(?=\.|,|\band\b|$)", text, re.I)
    if company:
        out["business_name"] = company.group(1).strip()
    cleaned = text.strip().strip(".,?!")
    words = cleaned.split()
    if requested_field == "full_name" and not out and 1 <= len(words) <= 4 and all(re.fullmatch(r"[A-Za-z]+", w) for w in words):
        if not any(w.casefold() in {"what", "how", "why", "when", "where", "documents", "required", "need", "loan", "business", "run", "want", "looking"} for w in words) and cleaned.casefold() not in {"yes", "no", "okay", "thanks", "retail", "equipment"}:
            out["full_name"] = cleaned
    if requested_field == "business_name" and not out and 1 <= len(words) <= 6 and all(re.fullmatch(r"[A-Za-z0-9&'-]+", w) for w in words):
        out["business_name"] = cleaned
    if requested_field == "business_type" and not out and len(words) <= 3 and re.fullmatch(r"[A-Za-z -]+", cleaned):
        out["business_type"] = cleaned.casefold().removesuffix(" business").strip()
    if requested_field == "loan_purpose" and not out and len(words) <= 4:
        purpose = next((x for x in ("equipment", "inventory", "working capital", "expansion") if x in t), None)
        if purpose:
            out["loan_purpose"] = purpose
    years = re.search(r"(?:about|around|nearly|for)\s+(\d+(?:\.\d+)?)\s+years?", t)
    if years:
        out["years_in_business"] = float(years.group(1))
    else:
        word_years = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
        years_words = re.search(r"(?:about|around|nearly|for)\s+([a-z]+)\s+years?", t)
        if years_words and years_words.group(1) in word_years:
            out["years_in_business"] = float(word_years[years_words.group(1)])
    if requested_field == "years_in_business" and "years_in_business" not in out:
        standalone = re.fullmatch(r"\s*(one|two|three|four|five|six|seven|eight|nine|ten|\d+(?:\.\d+)?)\s+years?\s*", t)
        if standalone:
            value = standalone.group(1)
            out["years_in_business"] = float({"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}.get(value, value))
    amount = re.search(r"(?:₹|rs\.?|inr\s*)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lacs|lac|million|crore|crores)?", t)
    if not amount:
        word_amounts = {"ten": 10, "twenty": 20, "twenty five": 25, "thirty": 30, "fifty": 50}
        for words, number in word_amounts.items():
            if words in t and any(w in t for w in ("loan", "borrow", "fund", "lakh", "amount")):
                amount = (number, "lakh")
                break
    if amount and any(w in t for w in ("loan", "borrow", "fund", "lakh", "crore", "amount")):
        value = float(amount.group(1).replace(",", "") if hasattr(amount, "group") else amount[0])
        unit = (amount.group(2) if hasattr(amount, "group") else amount[1]) or ""
        value *= {"lakh": 100000, "lakhs": 100000, "lacs": 100000, "lac": 100000, "million": 1000000, "crore": 10000000, "crores": 10000000}.get(unit, 1)
        out["requested_loan_amount"] = int(value)
    if requested_field == "requested_loan_amount" and "requested_loan_amount" not in out:
        standalone_amount = re.fullmatch(r"\s*(?:₹|rs\.?\s*)?([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lacs|lac|crore|crores)?\s*", t)
        if standalone_amount:
            value = float(standalone_amount.group(1).replace(",", ""))
            value *= {"lakh":100000,"lakhs":100000,"lacs":100000,"lac":100000,"crore":10000000,"crores":10000000}.get(standalone_amount.group(2) or "", 1)
            out["requested_loan_amount"] = int(value)
    if any(x in t for x in ("equipment", "inventory", "working capital", "expansion")):
        out["loan_purpose"] = next(x for x in ("equipment", "inventory", "working capital", "expansion") if x in t)
    return out


def evaluate(state) -> dict[str, Any]:
    rules = load_rules()
    fields = {**state.customer_profile, **state.business_details, **state.loan_requirement}
    missing = [f for f in rules["required_for_preliminary_review"] if not fields.get(f)]
    if state.conflicts:
        return {"state": "human_review", "missing": missing, "reason": "conflicting_information"}
    if missing:
        return {"state": "incomplete", "missing": missing}
    return {"state": "preliminary_qualified", "missing": [], "note": "Suitable for further discussion only; not approval."}

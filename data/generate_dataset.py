"""
Synthetic Bidder Dataset Generator
Generates ~150 fake companies with realistic, varied compliance profiles
for the AI-Powered Bid Compliance Verification Platform (SIH prototype).

Output:
  - bidders.json      -> full nested dataset (for mock APIs / backend)
  - bidders.csv        -> flat view (for quick inspection / Excel)
  - dataset_summary.md -> stats on how many bidders fall into each compliance bucket
"""

import json
import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # reproducible dataset

NUM_BIDDERS = 150

STATES = ["UP", "MH", "DL", "KA", "TN", "GJ", "RJ", "WB", "PB", "HR"]
CATEGORIES = ["Micro", "Small", "Medium"]
TENDER_CATEGORIES = ["Goods", "Services", "Works"]
COMPANY_SUFFIXES = ["Pvt Ltd", "Enterprises", "Industries", "Traders", "Solutions", "Technologies", "Corp", "Agro", "Textiles", "Engineering"]
COMPANY_PREFIXES = ["Shree", "National", "Bharat", "Global", "Sunrise", "Prime", "Apex", "Metro", "Unity", "Sterling",
                    "Vishnu", "Lakshmi", "Ganga", "Om", "Star", "United", "Modern", "Classic", "Royal", "Silver"]

def random_date(start_year=2018, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 8, 26)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def gen_gstin(state_code):
    state_num = str(STATES.index(state_code) + 1).zfill(2)
    pan_like = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + \
               ''.join(random.choices("0123456789", k=4)) + \
               random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return f"{state_num}{pan_like}1Z{random.randint(1,9)}"

def gen_pan():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + \
           ''.join(random.choices("0123456789", k=4)) + \
           random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def gen_udyam(state):
    return f"UDYAM-{state}-{random.randint(1,26):02d}-{random.randint(1000000,9999999)}"

def gen_cin():
    return f"U{random.randint(10000,99999)}DL{random.randint(2005,2023)}PTC{random.randint(100000,999999)}"

def weighted_status(compliant_weight=70, partial_weight=20, noncompliant_weight=10):
    return random.choices(
        ["COMPLIANT", "PARTIAL", "NON_COMPLIANT"],
        weights=[compliant_weight, partial_weight, noncompliant_weight]
    )[0]

def build_bidder(idx):
    state = random.choice(STATES)
    company_name = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    bidder_id = f"BID-{idx:05d}"
    category = random.choice(CATEGORIES)
    tender_category = random.choice(TENDER_CATEGORIES)

    # Assign an overall "profile" to make the dataset realistic and varied
    # 65% clean, 20% minor issues, 10% major issues, 5% blacklisted
    profile_roll = random.random()
    if profile_roll < 0.65:
        profile = "CLEAN"
    elif profile_roll < 0.85:
        profile = "MINOR_ISSUES"
    elif profile_roll < 0.95:
        profile = "MAJOR_ISSUES"
    else:
        profile = "BLACKLISTED"

    gstin = gen_gstin(state)
    pan = gen_pan()
    udyam = gen_udyam(state)
    cin = gen_cin()

    # --- GST Compliance ---
    if profile == "CLEAN":
        gst_status = "COMPLIANT"
        last_filed = random_date(2026, 2026)
        defaults = 0
    elif profile == "MINOR_ISSUES":
        gst_status = random.choice(["COMPLIANT", "PARTIAL"])
        last_filed = random_date(2025, 2026)
        defaults = random.randint(1, 2)
    elif profile == "MAJOR_ISSUES":
        gst_status = "NON_COMPLIANT"
        last_filed = random_date(2024, 2025)
        defaults = random.randint(3, 6)
    else:  # BLACKLISTED
        gst_status = random.choice(["COMPLIANT", "NON_COMPLIANT"])
        last_filed = random_date(2023, 2025)
        defaults = random.randint(0, 4)

    gst_check = {
        "check_type": "GST_COMPLIANCE",
        "status": gst_status,
        "details": {
            "gstin_valid": True,
            "registration_status": "Active" if gst_status != "NON_COMPLIANT" else "Suspended",
            "last_return_filed": last_filed.strftime("%Y-%m-%d"),
            "filing_defaults_last_12_months": defaults
        }
    }

    # --- PAN / ITR Compliance ---
    if profile == "CLEAN":
        itr_status = "COMPLIANT"
        itr_delay_days = 0
    elif profile == "MINOR_ISSUES":
        itr_status = "PARTIAL"
        itr_delay_days = random.randint(15, 60)
    elif profile == "MAJOR_ISSUES":
        itr_status = random.choice(["NON_COMPLIANT", "PARTIAL"])
        itr_delay_days = random.randint(60, 180)
    else:
        itr_status = random.choice(["COMPLIANT", "NON_COMPLIANT"])
        itr_delay_days = random.randint(0, 90)

    pan_check = {
        "check_type": "PAN_ITR_COMPLIANCE",
        "status": itr_status,
        "details": {
            "pan_valid": True,
            "itr_filed": itr_status != "NON_COMPLIANT",
            "filing_delay_days": itr_delay_days
        }
    }

    # --- Udyam / MSME ---
    if profile in ("CLEAN", "MINOR_ISSUES"):
        udyam_status = "COMPLIANT"
    elif profile == "MAJOR_ISSUES":
        udyam_status = random.choice(["PARTIAL", "NON_COMPLIANT"])
    else:
        udyam_status = random.choice(["COMPLIANT", "NON_COMPLIANT"])

    udyam_check = {
        "check_type": "UDYAM_MSME",
        "status": udyam_status,
        "details": {
            "udyam_number_valid": udyam_status != "NON_COMPLIANT",
            "category": category,
            "registration_active": udyam_status == "COMPLIANT"
        }
    }

    # --- EPFO/ESIC (not applicable for very small firms sometimes) ---
    epfo_applicable = random.random() > 0.15  # 15% chance not applicable (very small orgs)
    if not epfo_applicable:
        epfo_status = "NOT_APPLICABLE"
    elif profile == "CLEAN":
        epfo_status = "COMPLIANT"
    elif profile == "MINOR_ISSUES":
        epfo_status = random.choice(["COMPLIANT", "PARTIAL"])
    elif profile == "MAJOR_ISSUES":
        epfo_status = random.choice(["PARTIAL", "NON_COMPLIANT"])
    else:
        epfo_status = random.choice(["COMPLIANT", "NON_COMPLIANT"])

    epfo_check = {
        "check_type": "EPFO_ESIC_COMPLIANCE",
        "status": epfo_status,
        "details": {
            "applicable": epfo_applicable,
            "contribution_up_to_date": epfo_status == "COMPLIANT"
        }
    }

    # --- Make in India / Local content ---
    threshold = 50  # example tender requirement %
    if profile == "CLEAN":
        local_content_pct = random.randint(55, 95)
    elif profile == "MINOR_ISSUES":
        local_content_pct = random.randint(45, 60)
    elif profile == "MAJOR_ISSUES":
        local_content_pct = random.randint(20, 45)
    else:
        local_content_pct = random.randint(20, 90)

    mii_status = "COMPLIANT" if local_content_pct >= threshold else "NON_COMPLIANT"
    mii_check = {
        "check_type": "MAKE_IN_INDIA_LOCAL_CONTENT",
        "status": mii_status,
        "details": {
            "declared_local_content_percent": local_content_pct,
            "required_threshold_percent": threshold
        }
    }

    # --- Blacklist / Debarment ---
    is_blacklisted = (profile == "BLACKLISTED")
    blacklist_check = {
        "check_type": "BLACKLIST_DEBARMENT",
        "status": "NON_COMPLIANT" if is_blacklisted else "COMPLIANT",
        "details": {
            "is_blacklisted": is_blacklisted,
            "reason": random.choice([
                "Non-performance on previous contract",
                "Submission of fraudulent documents",
                "Debarred by Ministry order"
            ]) if is_blacklisted else None,
            "debarment_period": "2024-01-01 to 2027-01-01" if is_blacklisted else None
        }
    }

    bidder = {
        "bidder_id": bidder_id,
        "company_name": company_name,
        "gstin": gstin,
        "pan": pan,
        "udyam_number": udyam,
        "cin": cin,
        "registered_state": state,
        "msme_category": category,
        "tender_category": tender_category,
        "bid_id": f"GEM/2026/B/{random.randint(1000000,9999999)}",
        "submission_timestamp": random_date(2026, 2026).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile_tag": profile,  # for our own reference / testing, not shown to officer
        "compliance_checks": [
            gst_check, pan_check, udyam_check, epfo_check, mii_check, blacklist_check
        ]
    }
    return bidder


def compute_score(bidder):
    """Simple scoring engine matching the schema doc's weights."""
    weights = {
        "GST_COMPLIANCE": 20,
        "PAN_ITR_COMPLIANCE": 15,
        "UDYAM_MSME": 15,
        "EPFO_ESIC_COMPLIANCE": 15,
        "MAKE_IN_INDIA_LOCAL_CONTENT": 15,
        "BLACKLIST_DEBARMENT": 20
    }
    status_score = {"COMPLIANT": 1.0, "PARTIAL": 0.5, "NOT_APPLICABLE": 1.0, "NON_COMPLIANT": 0.0}

    total = 0
    blacklisted = False
    for check in bidder["compliance_checks"]:
        w = weights[check["check_type"]]
        s = status_score[check["status"]]
        total += w * s
        if check["check_type"] == "BLACKLIST_DEBARMENT" and check["status"] == "NON_COMPLIANT":
            blacklisted = True

    score = round(total)
    if blacklisted:
        risk = "HIGH"
        score = min(score, 30)  # cap score hard if blacklisted
    elif score >= 80:
        risk = "LOW"
    elif score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return score, risk


def main():
    bidders = [build_bidder(i + 1) for i in range(NUM_BIDDERS)]

    for b in bidders:
        score, risk = compute_score(b)
        b["reference_compliance_score"] = score
        b["reference_risk_level"] = risk

    # Save JSON (full nested structure)
    with open("/home/claude/bidders.json", "w") as f:
        json.dump(bidders, f, indent=2)

    # Save CSV (flattened, key fields only, for quick viewing)
    csv_fields = [
        "bidder_id", "company_name", "gstin", "pan", "udyam_number", "cin",
        "registered_state", "msme_category", "tender_category", "bid_id",
        "profile_tag", "reference_compliance_score", "reference_risk_level"
    ]
    with open("/home/claude/bidders.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for b in bidders:
            writer.writerow({k: b[k] for k in csv_fields})

    # Summary stats
    profile_counts = {}
    risk_counts = {}
    for b in bidders:
        profile_counts[b["profile_tag"]] = profile_counts.get(b["profile_tag"], 0) + 1
        risk_counts[b["reference_risk_level"]] = risk_counts.get(b["reference_risk_level"], 0) + 1

    with open("/home/claude/dataset_summary.md", "w") as f:
        f.write("# Synthetic Bidder Dataset — Summary\n\n")
        f.write(f"Total bidders generated: **{len(bidders)}**\n\n")
        f.write("## Profile distribution (ground truth, for testing your engine)\n\n")
        for k, v in profile_counts.items():
            f.write(f"- {k}: {v} ({round(100*v/len(bidders),1)}%)\n")
        f.write("\n## Computed risk level distribution (using reference scoring engine)\n\n")
        for k, v in risk_counts.items():
            f.write(f"- {k}: {v} ({round(100*v/len(bidders),1)}%)\n")
        f.write("\n## Sample bidder record\n\n```json\n")
        f.write(json.dumps(bidders[0], indent=2))
        f.write("\n```\n")

    print(f"Generated {len(bidders)} bidders.")
    print("Profile distribution:", profile_counts)
    print("Risk distribution:", risk_counts)


if __name__ == "__main__":
    main()
# Synthetic Bidder Dataset — Summary

Total bidders generated: **150**

## Profile distribution (ground truth, for testing your engine)

- CLEAN: 87 (58.0%)
- MAJOR_ISSUES: 25 (16.7%)
- MINOR_ISSUES: 29 (19.3%)
- BLACKLISTED: 9 (6.0%)

## Computed risk level distribution (using reference scoring engine)

- LOW: 105 (70.0%)
- HIGH: 34 (22.7%)
- MEDIUM: 11 (7.3%)

## Sample bidder record

```json
{
  "bidder_id": "BID-00001",
  "company_name": "Shree Solutions",
  "gstin": "02CTOPA0265W1Z9",
  "pan": "KLHWT1422Y",
  "udyam_number": "UDYAM-MH-11-2714803",
  "cin": "U22156DL2017PTC201414",
  "registered_state": "MH",
  "msme_category": "Micro",
  "tender_category": "Goods",
  "bid_id": "GEM/2026/B/5437923",
  "submission_timestamp": "2026-07-26T00:00:00Z",
  "profile_tag": "CLEAN",
  "compliance_checks": [
    {
      "check_type": "GST_COMPLIANCE",
      "status": "COMPLIANT",
      "details": {
        "gstin_valid": true,
        "registration_status": "Active",
        "last_return_filed": "2026-04-02",
        "filing_defaults_last_12_months": 0
      }
    },
    {
      "check_type": "PAN_ITR_COMPLIANCE",
      "status": "COMPLIANT",
      "details": {
        "pan_valid": true,
        "itr_filed": true,
        "filing_delay_days": 0
      }
    },
    {
      "check_type": "UDYAM_MSME",
      "status": "COMPLIANT",
      "details": {
        "udyam_number_valid": true,
        "category": "Micro",
        "registration_active": true
      }
    },
    {
      "check_type": "EPFO_ESIC_COMPLIANCE",
      "status": "COMPLIANT",
      "details": {
        "applicable": true,
        "contribution_up_to_date": true
      }
    },
    {
      "check_type": "MAKE_IN_INDIA_LOCAL_CONTENT",
      "status": "COMPLIANT",
      "details": {
        "declared_local_content_percent": 93,
        "required_threshold_percent": 50
      }
    },
    {
      "check_type": "BLACKLIST_DEBARMENT",
      "status": "COMPLIANT",
      "details": {
        "is_blacklisted": false,
        "reason": null,
        "debarment_period": null
      }
    }
  ],
  "reference_compliance_score": 100,
  "reference_risk_level": "LOW"
}
```
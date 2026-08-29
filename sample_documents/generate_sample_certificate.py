"""
Sample Certificate Generator
=============================
Generates realistic-looking (fake) certificate PDFs for a handful of
bidders from bidders.json: GST Registration Certificate, PAN Card,
and Udyam Registration Certificate.

These are NOT real government documents — purely synthetic layouts for
testing the AI Document Extraction module (Step 3) end-to-end without
needing real bidder uploads.

Run:
    python3 generate_sample_certificates.py
Output:
    sample_documents/<bidder_id>_gst_certificate.pdf
    sample_documents/<bidder_id>_pan_card.pdf
    sample_documents/<bidder_id>_udyam_certificate.pdf
"""

import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

OUT_DIR = os.path.join(os.path.dirname(__file__), "sample_documents")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(os.path.dirname(__file__), "bidders.json")) as f:
    BIDDERS = json.load(f)


def draw_header(c, title):
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40 * mm, title)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, height - 46 * mm, "Government of India (Simulated Sample Document for Prototype Testing Only)")
    c.line(30 * mm, height - 50 * mm, width - 30 * mm, height - 50 * mm)


def gst_certificate(bidder, path):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    draw_header(c, "GOODS AND SERVICES TAX CERTIFICATE OF REGISTRATION")

    gst_check = next(ch for ch in bidder["compliance_checks"] if ch["check_type"] == "GST_COMPLIANCE")
    y = height - 65 * mm
    lines = [
        ("Registration Number (GSTIN):", bidder["gstin"]),
        ("Legal Name of Business:", bidder["company_name"]),
        ("Trade Name:", bidder["company_name"]),
        ("Constitution of Business:", "Private Limited Company"),
        ("Address of Principal Place of Business:", f"{bidder['registered_state']}, India"),
        ("Date of Liability:", "01/04/2020"),
        ("Registration Status:", gst_check["details"]["registration_status"]),
        ("Last Return Filed On:", gst_check["details"]["last_return_filed"]),
    ]
    c.setFont("Helvetica", 11)
    for label, value in lines:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30 * mm, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(110 * mm, y, str(value))
        y -= 10 * mm

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(30 * mm, 20 * mm, "This is a system-generated synthetic certificate for SIH prototype testing. Not a valid legal document.")
    c.save()


def pan_card(bidder, path):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    draw_header(c, "INCOME TAX DEPARTMENT - PERMANENT ACCOUNT NUMBER CARD")

    pan_check = next(ch for ch in bidder["compliance_checks"] if ch["check_type"] == "PAN_ITR_COMPLIANCE")
    y = height - 65 * mm
    lines = [
        ("Permanent Account Number:", bidder["pan"]),
        ("Name:", bidder["company_name"]),
        ("Date of Incorporation:", "15/06/2016"),
        ("PAN Status:", "Valid" if pan_check["details"]["pan_valid"] else "Invalid"),
        ("Last ITR Filed:", "Yes" if pan_check["details"]["itr_filed"] else "No"),
        ("Filing Delay (days):", str(pan_check["details"]["filing_delay_days"])),
    ]
    c.setFont("Helvetica", 11)
    for label, value in lines:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30 * mm, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(110 * mm, y, str(value))
        y -= 10 * mm

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(30 * mm, 20 * mm, "This is a system-generated synthetic PAN record for SIH prototype testing. Not a valid legal document.")
    c.save()


def udyam_certificate(bidder, path):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    draw_header(c, "UDYAM REGISTRATION CERTIFICATE")

    udyam_check = next(ch for ch in bidder["compliance_checks"] if ch["check_type"] == "UDYAM_MSME")
    y = height - 65 * mm
    lines = [
        ("Udyam Registration Number:", bidder["udyam_number"]),
        ("Name of Enterprise:", bidder["company_name"]),
        ("Type of Enterprise:", bidder["msme_category"]),
        ("Date of Registration:", "10/09/2019"),
        ("Registration Status:", "Active" if udyam_check["details"]["registration_active"] else "Inactive"),
        ("Major Activity:", "Manufacturing" if bidder["tender_category"] == "Goods" else "Services"),
    ]
    c.setFont("Helvetica", 11)
    for label, value in lines:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30 * mm, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(110 * mm, y, str(value))
        y -= 10 * mm

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(30 * mm, 20 * mm, "This is a system-generated synthetic Udyam certificate for SIH prototype testing. Not a valid legal document.")
    c.save()


def main():
    # Generate documents for a handful of representative bidders:
    # one CLEAN, one MINOR_ISSUES, one MAJOR_ISSUES, one BLACKLISTED
    chosen = {}
    for b in BIDDERS:
        tag = b["profile_tag"]
        if tag not in chosen:
            chosen[tag] = b
        if len(chosen) == 4:
            break

    for tag, bidder in chosen.items():
        bid = bidder["bidder_id"]
        gst_certificate(bidder, os.path.join(OUT_DIR, f"{bid}_gst_certificate.pdf"))
        pan_card(bidder, os.path.join(OUT_DIR, f"{bid}_pan_card.pdf"))
        udyam_certificate(bidder, os.path.join(OUT_DIR, f"{bid}_udyam_certificate.pdf"))
        print(f"Generated 3 documents for {bid} ({tag}) — {bidder['company_name']}")

    # Save a small manifest so the extraction test script knows which bidder each file belongs to
    manifest = [
        {"bidder_id": b["bidder_id"], "profile_tag": tag, "company_name": b["company_name"]}
        for tag, b in chosen.items()
    ]
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
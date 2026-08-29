"""
AI Document Extraction Module
==============================
Step 3 of the pipeline: takes an uploaded bidder document (PDF), pulls
raw text out of it, then uses an LLM (Claude) to extract structured
fields (GSTIN, PAN, Udyam number, dates, statuses, etc.) as clean JSON —
regardless of how the document is laid out.

Why an LLM instead of pure regex?
  Real bidder-uploaded certificates vary wildly in layout, scan quality,
  and wording across states/years. A regex/template approach breaks the
  moment a document doesn't match the expected format. An LLM reads the
  document like a human would and returns consistent structured output
  even from messy or slightly different layouts — this is where "AI
  Document Verification" (Key Capability #2) actually earns its name.

Usage:
    export ANTHROPIC_API_KEY=your_key_here
    python3 extract_document.py sample_documents/BID-00001_gst_certificate.pdf GST_CERTIFICATE

Supported doc_type values:
    GST_CERTIFICATE, PAN_CARD, UDYAM_CERTIFICATE
"""

import sys
import os
import json
import pdfplumber

# The anthropic SDK is what your team will use in the real backend.
# pip install anthropic --break-system-packages
try:
    import anthropic
except ImportError:
    anthropic = None


EXTRACTION_SCHEMAS = {
    "GST_CERTIFICATE": {
        "fields": ["gstin", "legal_name", "trade_name", "registration_status", "last_return_filed_date"],
        "instructions": (
            "Extract the GSTIN (15-character GST Identification Number), legal name of business, "
            "trade name, registration status (Active/Suspended/Cancelled), and the last GST return "
            "filed date if mentioned."
        ),
    },
    "PAN_CARD": {
        "fields": ["pan", "name", "pan_status", "itr_filed", "filing_delay_days"],
        "instructions": (
            "Extract the PAN (10-character Permanent Account Number), the name on the PAN, "
            "PAN status (Valid/Invalid), whether the latest ITR was filed (true/false), and "
            "filing delay in days if mentioned."
        ),
    },
    "UDYAM_CERTIFICATE": {
        "fields": ["udyam_number", "enterprise_name", "enterprise_category", "registration_status"],
        "instructions": (
            "Extract the Udyam Registration Number, enterprise name, enterprise category "
            "(Micro/Small/Medium), and registration status (Active/Inactive)."
        ),
    },
}


def extract_text_from_pdf(file_path: str) -> str:
    """Step A: pull raw text out of the PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text.strip()


def build_prompt(doc_type: str, raw_text: str) -> str:
    schema = EXTRACTION_SCHEMAS[doc_type]
    fields_list = ", ".join(schema["fields"])
    return f"""You are a document data extraction engine for a government procurement compliance system.

Document type: {doc_type}
Task: {schema['instructions']}

Extract ONLY these fields: {fields_list}

Rules:
- Return ONLY valid JSON, no explanation, no markdown code fences.
- If a field is not found in the text, set its value to null.
- Also include a "confidence" field (0.0 to 1.0) reflecting how certain you are of the extraction overall.
- Also include an "extraction_notes" field (string) listing anything unusual, missing, or inconsistent you noticed.

Document text:
---
{raw_text}
---

Return JSON now:"""


def extract_with_claude(doc_type: str, raw_text: str, model: str = "claude-sonnet-4-6") -> dict:
    """Step B: send extracted text to Claude, get structured JSON back."""
    if anthropic is None:
        raise RuntimeError("anthropic SDK not installed. Run: pip install anthropic --break-system-packages")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
    prompt = build_prompt(doc_type, raw_text)

    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_reply = response.content[0].text.strip()
    # Defensive cleanup in case the model wraps output in code fences
    raw_reply = raw_reply.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw_reply)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse model output as JSON",
            "raw_output": raw_reply
        }


def extract_document(file_path: str, doc_type: str) -> dict:
    """Full pipeline: PDF -> raw text -> LLM extraction -> structured JSON."""
    if doc_type not in EXTRACTION_SCHEMAS:
        raise ValueError(f"Unsupported doc_type: {doc_type}. Must be one of {list(EXTRACTION_SCHEMAS.keys())}")

    raw_text = extract_text_from_pdf(file_path)
    if not raw_text:
        return {
            "extraction_status": "FAILED",
            "reason": "No extractable text found (likely a scanned image — route through OCR first, see pdf-reading skill)"
        }

    result = extract_with_claude(doc_type, raw_text)
    result["extraction_status"] = "SUCCESS" if "error" not in result else "FAILED"
    result["doc_type"] = doc_type
    result["source_file"] = os.path.basename(file_path)
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_document.py <pdf_path> <doc_type>")
        print(f"doc_type must be one of: {list(EXTRACTION_SCHEMAS.keys())}")
        sys.exit(1)

    pdf_path, doc_type = sys.argv[1], sys.argv[2]
    result = extract_document(pdf_path, doc_type)
    print(json.dumps(result, indent=2))
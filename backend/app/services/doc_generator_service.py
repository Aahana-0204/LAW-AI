import os

from .llm_service import call_llm

DOCUMENT_TEMPLATES = [
    {
        "id": "rental_agreement", "name": "Rental Agreement", "icon": "🏠",
        "description": "Residential/commercial property rental contract",
        "fields": ["landlord_name", "tenant_name", "property_address", "rent_amount", "duration", "city"],
    },
    {
        "id": "nda", "name": "Non-Disclosure Agreement", "icon": "🔒",
        "description": "Confidentiality agreement between parties",
        "fields": ["party1_name", "party2_name", "purpose", "duration", "city"],
    },
    {
        "id": "employment_contract", "name": "Employment Contract", "icon": "💼",
        "description": "Job offer and employment terms document",
        "fields": ["employer_name", "employee_name", "designation", "salary", "joining_date", "city"],
    },
    {
        "id": "legal_notice", "name": "Legal Notice", "icon": "📮",
        "description": "Formal legal notice to individual or organization",
        "fields": ["sender_name", "recipient_name", "subject", "details", "demand", "city"],
    },
    {
        "id": "affidavit", "name": "Affidavit", "icon": "✍️",
        "description": "Sworn statement for court or official use",
        "fields": ["deponent_name", "age", "address", "subject", "statements", "city"],
    },
    {
        "id": "poa", "name": "Power of Attorney", "icon": "⚖️",
        "description": "Authorization to act on someone's behalf",
        "fields": ["grantor_name", "attorney_name", "purpose", "scope", "city"],
    },
    {
        "id": "fir_complaint", "name": "FIR / Police Complaint", "icon": "🚔",
        "description": "First Information Report draft for police station",
        "fields": ["complainant_name", "incident_date", "location", "accused_name", "incident_details", "city"],
    },
    {
        "id": "consumer_complaint", "name": "Consumer Complaint", "icon": "🛒",
        "description": "Complaint to Consumer Forum / NCDRC",
        "fields": ["complainant_name", "company_name", "product_service", "issue_date", "complaint_details", "city"],
    },
    {
        "id": "rti_application", "name": "RTI Application", "icon": "📋",
        "description": "Right to Information request to government body",
        "fields": ["applicant_name", "address", "authority_name", "department", "information_sought", "city"],
    },
    {
        "id": "will_testament", "name": "Last Will & Testament", "icon": "📜",
        "description": "Legal will for asset distribution",
        "fields": ["testator_name", "age", "address", "beneficiaries", "assets_distribution", "executor_name", "city"],
    },
]


def get_templates() -> list:
    return DOCUMENT_TEMPLATES


def generate_document(template_id: str, fields: dict, custom_prompt: str = None) -> dict:
    template = next((t for t in DOCUMENT_TEMPLATES if t["id"] == template_id), None)

    if custom_prompt:
        prompt = f"""You are an expert Indian lawyer with 20 years of experience. Generate a complete, professional legal document based on this request.

REQUEST: {custom_prompt}

INSTRUCTIONS:
1. Generate a COMPLETE, properly formatted legal document
2. Use formal legal language appropriate for Indian law
3. Include all standard clauses for this document type
4. Proper headings, numbered sections, and structure
5. Reference applicable Indian statutes where relevant
6. Include signature blocks for all parties
7. Add a disclaimer at end: "This is an AI-generated draft. Consult a qualified lawyer before use."

Generate the complete document now:"""
    else:
        if not template:
            return {"error": f"Unknown template: {template_id}"}

        fields_text = "\n".join(
            f"- {k.replace('_', ' ').title()}: {v}"
            for k, v in fields.items() if v
        )

        prompt = f"""You are an expert Indian lawyer with 20 years of experience. Generate a complete, professional {template['name']} under Indian law.

DETAILS PROVIDED:
{fields_text}

INSTRUCTIONS:
1. Generate a COMPLETE, legally sound {template['name']} under Indian law
2. Formal legal language and tone throughout
3. Include ALL standard clauses for this document type in India
4. Properly numbered sections and sub-sections
5. Include recitals, operative clauses, and schedules where needed
6. Witness and signature blocks for all parties
7. Reference applicable Indian laws (Transfer of Property Act, Indian Contract Act, etc.)
8. At the end add: "DISCLAIMER: This document is AI-generated for reference only. Have it reviewed by a qualified advocate."

Generate the complete {template['name']}:"""

    try:
        content = call_llm(prompt, max_tokens=3000, temperature=0.1)
        return {
            "template_id": template_id,
            "template_name": template["name"] if template else "Custom Document",
            "content": content,
            "fields": fields,
        }
    except Exception as e:
        return {"error": f"Generation failed: {type(e).__name__}: {e}"}

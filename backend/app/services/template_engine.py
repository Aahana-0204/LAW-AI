"""
Intelligent legal response engine — no external API, no LLM.
Uses query intent detection + direct corpus extraction + procedure guides
to generate accurate, structured answers from the built-in legal corpus.
"""

import re

# ─── Domain metadata ──────────────────────────────────────────────────────────

DOMAIN_ACTS = {
    "Criminal": ["Indian Penal Code, 1860 (IPC)", "Code of Criminal Procedure, 1973 (CrPC)", "Indian Evidence Act, 1872"],
    "Constitutional": ["Constitution of India, 1950", "Protection of Human Rights Act, 1993"],
    "Family": ["Hindu Marriage Act, 1955", "Special Marriage Act, 1954", "Hindu Succession Act, 1956", "Protection of Women from Domestic Violence Act, 2005"],
    "Property": ["Transfer of Property Act, 1882", "Registration Act, 1908", "Indian Stamp Act, 1899"],
    "Labour": ["Industrial Disputes Act, 1947", "Minimum Wages Act, 1948", "Payment of Gratuity Act, 1972", "Employees' Provident Funds Act, 1952"],
    "Corporate": ["Companies Act, 2013", "SEBI Act, 1992", "Insolvency and Bankruptcy Code, 2016"],
    "Tax": ["Income Tax Act, 1961", "Goods and Services Tax Act, 2017", "Central Excise Act, 1944"],
    "Consumer": ["Consumer Protection Act, 2019", "Prevention of Food Adulteration Act"],
    "Cyber": ["Information Technology Act, 2000", "IT (Amendment) Act, 2008"],
    "General": ["Constitution of India", "Indian Contract Act, 1872", "Code of Civil Procedure, 1908"],
}

DOMAIN_COURTS = {
    "Criminal": "Sessions Court → High Court → Supreme Court",
    "Constitutional": "High Court (Article 226) / Supreme Court (Article 32)",
    "Family": "Family Court → District Court → High Court",
    "Property": "Civil Court / Revenue Court → High Court",
    "Labour": "Labour Court / Industrial Tribunal → High Court",
    "Corporate": "National Company Law Tribunal (NCLT) → NCLAT → Supreme Court",
    "Tax": "Income Tax Appellate Tribunal (ITAT) → High Court → Supreme Court",
    "Consumer": "District Consumer Commission (≤₹1Cr) → State Commission → National Commission",
    "General": "Civil Court → High Court → Supreme Court",
}

# ─── Out-of-domain guard ──────────────────────────────────────────────────────

OUT_OF_DOMAIN_TEMPLATE = (
    "🚫 **Outside My Domain**\n\n"
    "I am LAWAI — an AI assistant specializing **exclusively in Indian law**.\n\n"
    "I cannot answer questions about cricket, sports, weather, cooking, entertainment, "
    "science, technology, or other non-legal topics.\n\n"
    "**Ask me about:**\n"
    "- 🔴 IPC sections & criminal law\n"
    "- 📜 Constitutional rights (Articles 12–35)\n"
    "- 👨‍👩‍👧 Family law (divorce, custody, maintenance)\n"
    "- 🏠 Property & rent disputes\n"
    "- 💼 Employment & labour law\n"
    "- 🏢 Company law & compliance\n"
    "- 💰 Tax law (GST, Income Tax)\n"
    "- 👥 Consumer rights & protection"
)

MIN_RELEVANCE_THRESHOLD = 20

# ─── Step-by-step procedure guides ───────────────────────────────────────────

PROCEDURE_GUIDES = {
    "fir": {
        "title": "How to File an FIR",
        "law": "Section 154 CrPC — Information in Cognizable Cases",
        "steps": [
            "**Step 1 — Go to the right police station**: Visit the station having jurisdiction over the place where the crime occurred.",
            "**Step 2 — Narrate the incident**: Give a clear oral or written account of the offence, including date, time, place, persons involved, and witnesses.",
            "**Step 3 — FIR is recorded**: The officer must record the information in the FIR register, read it back to you, and you sign/thumb-mark it.",
            "**Step 4 — Get your free copy**: You are entitled to a free copy of the FIR under Section 154(2) CrPC. Demand it.",
            "**Step 5 — If police refuse**: (a) Send complaint by post to the Superintendent of Police, or (b) file a private complaint before the Magistrate under Section 156(3) CrPC, or (c) approach the High Court.",
        ],
        "note": "Police CANNOT refuse to register an FIR for a cognizable offence — it is a statutory duty. Zero FIR (filed at any station) is valid and must be transferred."
    },
    "bail": {
        "title": "How to Apply for Bail",
        "law": "Sections 436–439 CrPC",
        "steps": [
            "**Step 1 — Determine offence type**: Bailable offences (Sec 436) → bail as of right. Non-bailable (Sec 437) → apply to Magistrate/Sessions Court.",
            "**Step 2 — Engage a lawyer**: File a bail application before the competent court (Magistrate for most cases; Sessions Court for serious offences).",
            "**Step 3 — Bail application**: The application must state grounds — no flight risk, no tampering risk, first offence, health, family grounds, etc.",
            "**Step 4 — Court hearing**: Prosecution presents objections; court considers gravity of offence, criminal antecedents, and grounds given.",
            "**Step 5 — If refused**: Appeal to Sessions Court (if Magistrate refused), then High Court under Section 439 CrPC.",
        ],
        "note": "Anticipatory bail (Section 438 CrPC) can be sought BEFORE arrest if there is reason to believe arrest is imminent."
    },
    "divorce": {
        "title": "How to File for Divorce in India",
        "law": "Hindu Marriage Act, 1955 (Section 13 & 13B); Special Marriage Act, 1954",
        "steps": [
            "**Step 1 — Determine type**: Mutual Consent (both agree) → faster. Contested (one party objects) → longer process.",
            "**Step 2 — Mutual Consent (Section 13B HMA)**: Both parties jointly file petition in Family Court. Court grants 6-month cooling-off period (can be waived). File second motion. Court passes decree.",
            "**Step 3 — Contested Divorce (Section 13 HMA)**: File petition citing grounds: cruelty, desertion (2 years), adultery, unsound mind, leprosy, venereal disease, conversion, or renunciation.",
            "**Step 4 — Court proceedings**: Serving notice → Written statement → Evidence → Arguments → Decree.",
            "**Step 5 — Maintenance & custody**: Apply separately or along with divorce petition for maintenance (Section 125 CrPC / Section 24 HMA) and child custody.",
        ],
        "note": "Mutual consent divorce typically takes 6–18 months. Contested divorce may take 2–5 years. Mediation is encouraged by courts."
    },
    "consumer_complaint": {
        "title": "How to File a Consumer Complaint",
        "law": "Consumer Protection Act, 2019",
        "steps": [
            "**Step 1 — Send legal notice**: Send a written complaint to the company/service provider first, giving 15–30 days to resolve.",
            "**Step 2 — Choose the right forum**: District Commission (claims up to ₹1 crore), State Commission (₹1–10 crore), National Commission (above ₹10 crore).",
            "**Step 3 — File complaint**: Submit complaint with copies of bills, receipts, correspondence, and legal notice. Pay nominal fee.",
            "**Step 4 — Admission and notice**: Commission admits the complaint and sends notice to the opposite party.",
            "**Step 5 — Hearing and order**: Both sides present arguments. Commission orders refund, replacement, compensation, or penalty.",
        ],
        "note": "You can also file online at consumerhelpline.gov.in (National Consumer Helpline: 1800-11-4000). No lawyer required for District Commission."
    },
    "employment_termination": {
        "title": "Rights When Fired / Terminated Without Notice",
        "law": "Industrial Disputes Act, 1947; Shops & Establishment Acts; IPC Section 406/420",
        "steps": [
            "**Step 1 — Check your contract**: Review employment contract for notice period, termination clause, and severance terms.",
            "**Step 2 — Demand notice pay**: If terminated without notice, you are entitled to salary in lieu of notice period (usually 1–3 months).",
            "**Step 3 — Claim dues**: Ensure all dues are paid — pending salary, leave encashment, provident fund (PF), and gratuity (if >5 years service).",
            "**Step 4 — File complaint**: For companies with 100+ workers, retrenchment without prior government permission is illegal. File complaint with Labour Commissioner.",
            "**Step 5 — Approach Labour Court**: File under the Industrial Disputes Act for reinstatement or compensation within 3 years.",
        ],
        "note": "Under Section 25F of the Industrial Disputes Act, a workman must receive 1 month's notice OR salary in lieu, plus retrenchment compensation of 15 days' salary per year of service."
    },
    "cheque_bounce": {
        "title": "How to Handle Cheque Bounce (Section 138 NI Act)",
        "law": "Section 138, Negotiable Instruments Act, 1881",
        "steps": [
            "**Step 1 — Bank memo**: Collect the cheque return memo from your bank stating the reason for dishonour.",
            "**Step 2 — Send legal notice**: Send a written demand notice to the drawer within 30 days of receiving the bank memo, demanding payment within 15 days.",
            "**Step 3 — Wait 15 days**: If payment is not made within 15 days of receiving the notice, the offence is complete.",
            "**Step 4 — File complaint**: File a criminal complaint before the Magistrate within 30 days of expiry of the 15-day notice period.",
            "**Step 5 — Court proceedings**: Cheque bounce is a criminal offence — punishment up to 2 years imprisonment AND/OR fine up to twice the cheque amount.",
        ],
        "note": "Time limits are strict — missing the 30-day notice window or 30-day complaint window bars the case. Keep all bank statements and courier receipts."
    },
    "property_registration": {
        "title": "How to Register Property / Sale Deed",
        "law": "Registration Act, 1908; Transfer of Property Act, 1882; Stamp Act",
        "steps": [
            "**Step 1 — Verify title**: Get an Encumbrance Certificate (EC) from the Sub-Registrar office to confirm no pending loans or disputes.",
            "**Step 2 — Draft sale deed**: Have a lawyer draft the sale deed with all details — parties, property description, consideration amount.",
            "**Step 3 — Pay stamp duty**: Pay stamp duty (varies by state: 3–8% of property value) and get stamp paper.",
            "**Step 4 — Registration**: Both buyer and seller appear before the Sub-Registrar of Assurances with 2 witnesses and original documents.",
            "**Step 5 — Mutation**: After registration, apply for mutation (change of name) in the municipal/revenue records.",
        ],
        "note": "Unregistered sale deeds are NOT valid for immovable property worth more than ₹100 under Section 17 of the Registration Act."
    },
    "domestic_violence": {
        "title": "How to File a Domestic Violence Complaint",
        "law": "Protection of Women from Domestic Violence Act, 2005 (PWDVA); IPC Section 498A",
        "steps": [
            "**Step 1 — Contact a Protection Officer**: Every district has a Protection Officer. File a Domestic Incident Report (DIR) with them.",
            "**Step 2 — File police complaint**: Lodge FIR under Section 498A IPC (cruelty by husband/relatives) at the local police station.",
            "**Step 3 — Apply to Magistrate**: File application under PWDVA for Protection Order, Residence Order, Monetary Relief, or Custody Order.",
            "**Step 4 — Emergency relief**: Courts can grant interim protection orders on the same day to prevent further violence.",
            "**Step 5 — Support services**: Contact One Stop Centre (Sakhi) at any district hospital or call helpline 181 (Women Helpline) for shelter, legal aid, and counselling.",
        ],
        "note": "Under PWDVA, the aggrieved woman cannot be evicted from the shared household even if she has no ownership rights."
    },
}

# Keywords that trigger procedure guides
PROCEDURE_TRIGGERS = {
    "fir": ["file fir", "file a fir", "lodge fir", "register fir", "file complaint police", "how to report crime", "how to file fir"],
    "bail": ["apply for bail", "get bail", "how to get bail", "bail application", "apply bail"],
    "divorce": ["file for divorce", "file divorce", "how to divorce", "divorce procedure", "how to get divorce", "mutual consent divorce"],
    "consumer_complaint": ["consumer complaint", "file consumer", "consumer forum", "cheated by company", "product defective", "service complaint"],
    "employment_termination": ["fired without notice", "terminated without notice", "wrongful termination", "illegal termination", "employer fired me", "boss fired me", "job terminated"],
    "cheque_bounce": ["cheque bounce", "check bounce", "cheque dishonour", "bounced cheque", "section 138"],
    "property_registration": ["register property", "property registration", "sale deed", "register land", "register flat"],
    "domestic_violence": ["domestic violence", "file domestic violence", "husband beating", "wife beating", "498a", "section 498"],
}

# ─── Query analysis helpers ───────────────────────────────────────────────────

def _detect_intent(query: str) -> str:
    q = query.lower()
    if re.search(r'\b(punish|penalty|sentence|fine|jail|prison|liable|how many year|what year|imprisonment)\b', q):
        return 'punishment'
    if re.search(r'\b(how to|how do i|procedure|step|process|file|apply|complaint|what should i do|what can i do|what to do)\b', q):
        return 'procedure'
    if re.search(r'\b(my right|what right|can i|am i allowed|am i entitled|legal right|entitle|protect)\b', q):
        return 'rights'
    if re.search(r'\b(difference|vs\b|versus|compare|between)\b', q):
        return 'comparison'
    if re.search(r'\b(what is|define|meaning|explain|tell me about|describe)\b', q):
        return 'definition'
    return 'general'


def _match_procedure(query: str):
    """Return a procedure guide dict or None."""
    q = query.lower()
    for key, triggers in PROCEDURE_TRIGGERS.items():
        for trigger in triggers:
            if trigger in q:
                return PROCEDURE_GUIDES[key]
    return None


def _extract_sentences_by_intent(content: str, intent: str) -> list:
    """Pull the most relevant sentences from corpus content based on what user wants."""
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', content) if len(s.strip()) > 15]

    if intent == 'punishment':
        keywords = ['punish', 'imprison', 'fine', 'death', 'liable', 'sentence', 'year', 'month', 'life imprisonment']
    elif intent == 'rights':
        keywords = ['right', 'entitle', 'protect', 'guaranteed', 'free', 'cannot', 'shall not', 'duty', 'access']
    elif intent == 'procedure':
        keywords = ['file', 'apply', 'submit', 'court', 'procedure', 'complaint', 'petition', 'step', 'magistrate']
    else:
        return sentences  # return all for definition/general

    scored = []
    for s in sentences:
        sl = s.lower()
        score = sum(1 for kw in keywords if kw in sl)
        scored.append((score, s))
    scored.sort(reverse=True)

    top = [s for sc, s in scored if sc > 0]
    return top if top else sentences


# ─── Main response generator ──────────────────────────────────────────────────

def generate_template_response(query: str, domain: str, corpus_results: list) -> str:
    """
    Generate an accurate, structured legal response.
    Uses direct corpus lookup + intent detection + procedure guides.
    No LLM, no external API.
    """

    # ── Out-of-domain guard ───────────────────────────────────────────────
    if domain == "General":
        top_relevance = corpus_results[0]["relevance"] if corpus_results else 0
        if top_relevance < MIN_RELEVANCE_THRESHOLD:
            return OUT_OF_DOMAIN_TEMPLATE

    acts = DOMAIN_ACTS.get(domain, DOMAIN_ACTS["General"])
    court = DOMAIN_COURTS.get(domain, DOMAIN_COURTS["General"])
    intent = _detect_intent(query)
    lines = []

    # ── Check for procedural how-to query ────────────────────────────────
    guide = _match_procedure(query)
    if guide or intent == 'procedure':
        if guide:
            lines.append(f"## 📋 {guide['title']}\n")
            lines.append(f"**Governing Law:** {guide['law']}\n")
            lines.append("### Steps:\n")
            for step in guide['steps']:
                lines.append(step + "\n")
            lines.append(f"\n> 💡 **Note:** {guide['note']}\n")
        else:
            # Generic procedure guidance from corpus
            lines.append(f"## 📋 Legal Procedure — {domain} Law\n")
            if corpus_results:
                top = corpus_results[0]
                relevant = _extract_sentences_by_intent(top['content'], 'procedure')
                lines.append(f"**Applicable Law:** {top['title']}\n")
                for s in relevant[:4]:
                    lines.append(f"- {s}")
                lines.append("")

        # Append relevant corpus sections below the guide
        if corpus_results:
            lines.append("\n## ⚖️ Relevant Legal Provisions\n")
            for r in corpus_results[:3]:
                lines.append(f"### {r['title']}")
                lines.append(r['content'] + "\n")

        lines.append("\n## 📋 Applicable Acts\n")
        for act in acts:
            lines.append(f"- {act}")

        lines.append(f"\n\n---\n> ⚠️ **Important:** This is legal information, not legal advice. "
                     f"For your specific situation, consult a lawyer registered with the Bar Council of India.")
        return "\n".join(lines)

    # ── Specific section / article query (definition or punishment) ───────
    if corpus_results and corpus_results[0]["relevance"] >= 90:
        top = corpus_results[0]
        relevant_sentences = _extract_sentences_by_intent(top['content'], intent)

        if intent == 'punishment':
            lines.append(f"## ⚖️ Punishment under {top['title']}\n")
            if relevant_sentences:
                for s in relevant_sentences[:4]:
                    lines.append(f"- {s}")
            else:
                lines.append(top['content'])
        else:
            lines.append(f"## ⚖️ {top['title']}\n")
            lines.append(top['content'] + "\n")

        # Add related sections
        if len(corpus_results) > 1:
            lines.append("\n## 🔗 Related Provisions\n")
            for r in corpus_results[1:3]:
                lines.append(f"### {r['title']}")
                rel = _extract_sentences_by_intent(r['content'], intent)
                lines.append("\n".join(rel[:3]) + "\n")

        lines.append("\n## 📋 Governing Acts\n")
        for act in acts:
            lines.append(f"- {act}")
        lines.append(f"\n**Forum:** {court}")

        # Key takeaway
        lines.append("\n## 🔑 Key Takeaway\n")
        lines.append(f"- **Section/Provision:** {top.get('section', top['title'])}")
        lines.append(f"- **Domain:** {domain} Law")
        if relevant_sentences:
            lines.append(f"- {relevant_sentences[0][:200]}")

        lines.append(f"\n\n---\n> ⚠️ **Important:** Laws may be amended — always verify with official sources or a qualified advocate.")
        return "\n".join(lines)

    # ── General / multi-source answer ─────────────────────────────────────
    lines.append(f"## ⚖️ Legal Answer — {domain} Law\n")

    if corpus_results:
        top = corpus_results[0]
        relevant_sentences = _extract_sentences_by_intent(top['content'], intent)

        lines.append(f"**{top['title']}**\n")
        if intent in ('punishment', 'rights') and relevant_sentences:
            for s in relevant_sentences[:4]:
                lines.append(f"- {s}")
        else:
            lines.append(top['content'] + "\n")

        if len(corpus_results) > 1:
            lines.append(f"\n**Also relevant — {corpus_results[1]['title']}**\n")
            lines.append(corpus_results[1]['content'][:400] +
                         ("..." if len(corpus_results[1]['content']) > 400 else "") + "\n")
    else:
        lines.append(
            f"This query relates to **{domain} Law** under the Indian legal framework. "
            f"The relevant provisions are governed by the acts listed below. "
            f"Please consult a qualified advocate for specific legal advice.\n"
        )

    lines.append("\n## 📋 Relevant Acts & Provisions\n")
    for act in acts:
        lines.append(f"- {act}")

    lines.append("\n## 🔑 Key Points\n")
    if corpus_results:
        for r in corpus_results[:4]:
            snippet = r['snippet'][:150].rstrip('.') + '.'
            lines.append(f"- **{r['section'] or r['title']}** — {snippet}")
    else:
        lines.append(f"- Governed by {domain} Law jurisdiction in India")
        lines.append("- Courts follow hierarchical structure: District → High Court → Supreme Court")
        lines.append("- Free legal aid available under Legal Services Authorities Act, 1987")

    lines.append("\n## 💡 Practical Guidance\n")
    lines.append(
        f"- **Where to go:** {court}\n"
        f"- **Primary Act:** {acts[0]}\n"
        f"- **Free Legal Aid:** Available at every District Legal Services Authority (DLSA)\n"
        f"- **National Helpline:** Dial **15100** (National Legal Services Authority)"
    )

    lines.append(f"\n\n---\n> ⚠️ **Important:** This is legal information, not legal advice. "
                 f"Laws may be amended — always verify with official sources or consult a lawyer registered "
                 f"with the Bar Council of India.")
    return "\n".join(lines)

"""
Template-based legal response engine.
Generates structured legal answers from corpus search results.
Zero dependencies, zero API calls, works 100% offline forever.

Used when LLM_BACKEND=template (default fallback when no LLM API is configured).
"""

from .corpus_search import search_corpus
from .domain_classifier import classify_domain

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
    "Criminal": "Sessions Court / High Court / Supreme Court",
    "Constitutional": "High Court (Article 226) / Supreme Court (Article 32)",
    "Family": "Family Court / District Court",
    "Property": "Civil Court / Revenue Court",
    "Labour": "Labour Court / Industrial Tribunal",
    "Corporate": "National Company Law Tribunal (NCLT) / SEBI",
    "Tax": "Income Tax Appellate Tribunal / High Court",
    "Consumer": "District Consumer Forum / State Commission / National Commission",
    "General": "Civil Court / High Court",
}


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

# Minimum relevance score (0-100) for the top corpus result to be considered legal
MIN_RELEVANCE_THRESHOLD = 20


def generate_template_response(query: str, domain: str, corpus_results: list) -> str:
    """
    Generate a structured legal response from corpus search results.
    No external API needed — uses the pre-built legal corpus.
    Returns an out-of-domain message if relevance is too low.
    """
    # Guard: if best match relevance is below threshold AND domain is General
    # it means the corpus has no meaningful legal match → out of domain
    if domain == "General":
        top_relevance = corpus_results[0]["relevance"] if corpus_results else 0
        if top_relevance < MIN_RELEVANCE_THRESHOLD:
            return OUT_OF_DOMAIN_TEMPLATE

    acts = DOMAIN_ACTS.get(domain, DOMAIN_ACTS["General"])
    court = DOMAIN_COURTS.get(domain, DOMAIN_COURTS["General"])

    # Build context from corpus results
    has_results = len(corpus_results) > 0

    lines = []

    # ─── Legal Position ───
    lines.append("## ⚖️ Legal Position\n")
    if has_results:
        top = corpus_results[0]
        lines.append(f"**{top['title']}**\n")
        lines.append(top["content"] + "\n")
        if len(corpus_results) > 1:
            second = corpus_results[1]
            lines.append(f"\n**Related: {second['title']}**\n")
            lines.append(second["content"][:400] + ("..." if len(second["content"]) > 400 else "") + "\n")
    else:
        lines.append(
            f"This query relates to **{domain} Law** under Indian legal framework. "
            f"The relevant legal provisions are governed by the acts listed below. "
            f"For precise legal advice tailored to your specific situation, "
            f"consulting a qualified advocate is strongly recommended.\n"
        )

    # ─── Relevant Provisions ───
    lines.append("\n## 📋 Relevant Acts & Provisions\n")
    for act in acts:
        lines.append(f"- {act}")
    lines.append("")

    # ─── Key Points ───
    lines.append("\n## 🔑 Key Points\n")
    if has_results:
        for r in corpus_results[:4]:
            lines.append(f"- **{r['section']}** — {r['snippet'][:120]}{'...' if len(r['snippet']) > 120 else ''}")
    else:
        lines.append(f"- The query falls under **{domain} Law** jurisdiction in India")
        lines.append("- Indian courts follow a hierarchical structure from District to Supreme Court")
        lines.append("- Legal proceedings must follow procedures laid down in applicable procedural codes")
        lines.append("- Time limitations (Limitation Act, 1963) apply to most legal actions")
    lines.append("")

    # ─── Practical Implications ───
    lines.append("\n## 💡 Practical Implications\n")
    lines.append(
        f"- **Jurisdiction**: Matters can be taken before the {court}\n"
        f"- **Applicable Law**: Primarily governed by {acts[0]}\n"
        f"- **Legal Aid**: Free legal aid is available under the Legal Services Authorities Act, 1987\n"
        f"- **Documentation**: Maintain all relevant records, agreements, and correspondence as evidence"
    )

    # ─── Important Note ───
    lines.append("\n\n---\n> ⚠️ **Important Note**: This information is based on the Indian legal corpus. "
                 "Laws may be amended — always verify with official sources or a qualified advocate. "
                 "For specific legal situations, consult a lawyer registered with the Bar Council of India.")

    return "\n".join(lines)

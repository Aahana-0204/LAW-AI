from flask import Blueprint, jsonify

docs_bp = Blueprint("docs", __name__)

LEGAL_DOMAINS = [
    {
        "id": "criminal",
        "name": "Criminal Law",
        "icon": "⚖️",
        "description": "IPC, CrPC, bail, FIR, arrest",
        "color": "red",
    },
    {
        "id": "civil",
        "name": "Civil Law",
        "icon": "📜",
        "description": "Contracts, property disputes, torts",
        "color": "blue",
    },
    {
        "id": "constitutional",
        "name": "Constitutional Law",
        "icon": "🏛️",
        "description": "Fundamental rights, PIL, writs",
        "color": "purple",
    },
    {
        "id": "family",
        "name": "Family Law",
        "icon": "👨‍👩‍👧",
        "description": "Divorce, custody, maintenance",
        "color": "green",
    },
    {
        "id": "property",
        "name": "Property Law",
        "icon": "🏠",
        "description": "Land, registry, tenancy, mortgage",
        "color": "orange",
    },
    {
        "id": "labour",
        "name": "Labour Law",
        "icon": "👷",
        "description": "Employment, wages, workplace rights",
        "color": "yellow",
    },
    {
        "id": "corporate",
        "name": "Corporate Law",
        "icon": "🏢",
        "description": "Company law, compliance, M&A",
        "color": "cyan",
    },
    {
        "id": "tax",
        "name": "Tax Law",
        "icon": "💰",
        "description": "Income tax, GST, TDS, ITR",
        "color": "emerald",
    },
]


@docs_bp.route("/domains", methods=["GET"])
def domains():
    return jsonify({"domains": LEGAL_DOMAINS}), 200

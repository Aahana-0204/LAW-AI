"""
Indian Legal Document Generator.
Generates complete, properly formatted legal documents using
embedded templates + field substitution. No LLM, no external API.
All documents follow Indian law standards.
"""

from datetime import datetime

# ─── Template metadata ────────────────────────────────────────────────────────

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

DISCLAIMER = (
    "\n\n" + "=" * 70 + "\n"
    "DISCLAIMER: This document is AI-generated for reference and informational\n"
    "purposes only. It does not constitute legal advice. Please have this\n"
    "document reviewed and executed under the supervision of a qualified\n"
    "advocate registered with the Bar Council of India before use.\n"
    "=" * 70
)

# ─── Complete document templates ──────────────────────────────────────────────

def _rental_agreement(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
RENTAL AGREEMENT
================================================================================

This Rental Agreement ("Agreement") is entered into on this {date}, at {f.get('city', '[City]')}.

BETWEEN:

LANDLORD:
{f.get('landlord_name', '[Landlord Name]')}
(hereinafter referred to as "the Landlord")

AND

TENANT:
{f.get('tenant_name', '[Tenant Name]')}
(hereinafter referred to as "the Tenant")

WHEREAS the Landlord is the lawful owner of the premises described below and is
willing to let the same on rent, and the Tenant is desirous of taking the said
premises on rent, both parties agree as follows:

================================================================================
SCHEDULE OF PROPERTY
================================================================================

Property Address: {f.get('property_address', '[Property Address]')}
City: {f.get('city', '[City]')}

================================================================================
TERMS AND CONDITIONS
================================================================================

1. TERM OF TENANCY
   1.1 This Agreement shall be for a period of {f.get('duration', '11 months')}, commencing
       from the date of execution hereof, unless earlier terminated in accordance
       with the provisions herein.
   1.2 Thereafter, this Agreement may be renewed by mutual written consent of both parties.

2. RENT
   2.1 The monthly rent payable for the said premises shall be Rs. {f.get('rent_amount', '[Amount]')}
       (Rupees {f.get('rent_amount', '[Amount]')} Only).
   2.2 The rent shall be paid on or before the 5th day of each calendar month.
   2.3 Any delay in payment beyond the 5th shall attract a late payment charge
       of 2% per month on the outstanding amount.

3. SECURITY DEPOSIT
   3.1 The Tenant shall deposit an interest-free refundable security deposit
       equivalent to two (2) months' rent at the time of execution of this Agreement.
   3.2 The security deposit shall be refunded within 30 days of vacating the premises,
       after deducting any outstanding dues or damages caused by the Tenant.

4. MAINTENANCE AND UTILITIES
   4.1 The Tenant shall bear the cost of electricity, water, and other utility charges.
   4.2 Minor day-to-day repairs up to Rs. 500/- shall be borne by the Tenant.
   4.3 Major structural repairs shall be the responsibility of the Landlord.
   4.4 The Tenant shall not make any structural alterations to the premises without
       the prior written consent of the Landlord.

5. USE OF PREMISES
   5.1 The premises shall be used for residential purposes only.
   5.2 The Tenant shall not sub-let, assign, or part with possession of the premises
       or any part thereof without the prior written consent of the Landlord.
   5.3 The Tenant shall not use the premises for any illegal, immoral, or unlawful purpose.
   5.4 The Tenant shall not store any hazardous or inflammable materials on the premises.

6. INSPECTION
   6.1 The Landlord or their authorized representative shall have the right to inspect
       the premises at any reasonable time after giving 24 hours prior notice.

7. TERMINATION
   7.1 Either party may terminate this Agreement by giving one (1) month's prior written notice.
   7.2 In case of breach of any terms of this Agreement, the aggrieved party may
       terminate this Agreement by giving 15 days' notice to remedy the breach.
   7.3 Upon expiry or termination, the Tenant shall peacefully hand over possession
       of the premises to the Landlord in the same condition as received, subject
       to normal wear and tear.

8. GOVERNING LAW
   8.1 This Agreement shall be governed by and construed in accordance with the
       laws of India, including the Transfer of Property Act, 1882, and the
       Rent Control Act applicable in {f.get('city', 'the city')}.
   8.2 Any disputes arising out of this Agreement shall be subject to the exclusive
       jurisdiction of the courts in {f.get('city', '[City]')}.

9. MISCELLANEOUS
   9.1 This Agreement constitutes the entire agreement between the parties and
       supersedes all prior negotiations, representations, and understandings.
   9.2 Any modification to this Agreement must be in writing and signed by both parties.
   9.3 If any provision of this Agreement is held to be invalid, the remaining
       provisions shall continue to be valid and enforceable.

================================================================================
SIGNATURES
================================================================================

IN WITNESS WHEREOF, both parties have set their hands on the date first above written.

LANDLORD:                                   TENANT:

____________________________                ____________________________
{f.get('landlord_name', '[Landlord Name]')}                     {f.get('tenant_name', '[Tenant Name]')}
Date: ____________________                  Date: ____________________


WITNESSES:

1. ____________________________             2. ____________________________
   Name: ____________________                 Name: ____________________
   Address: __________________                Address: __________________
   Date: _____________________                Date: _____________________

Place: {f.get('city', '[City]')}
{DISCLAIMER}"""


def _nda(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
NON-DISCLOSURE AGREEMENT (NDA)
================================================================================

This Non-Disclosure Agreement ("Agreement") is entered into as of {date},

BETWEEN:

DISCLOSING PARTY:
{f.get('party1_name', '[Party 1 Name]')}
(hereinafter referred to as "the Disclosing Party")

AND

RECEIVING PARTY:
{f.get('party2_name', '[Party 2 Name]')}
(hereinafter referred to as "the Receiving Party")

(Individually referred to as a "Party" and collectively as "the Parties")

PURPOSE: {f.get('purpose', '[Purpose of disclosure]')}

================================================================================
TERMS AND CONDITIONS
================================================================================

1. DEFINITION OF CONFIDENTIAL INFORMATION
   "Confidential Information" means any and all information or data that has or
   could have commercial value or other utility in the business in which the
   Disclosing Party is engaged. If Confidential Information is in written form,
   the Disclosing Party shall label or stamp the materials with the word
   "Confidential" or some similar warning.

2. OBLIGATIONS OF THE RECEIVING PARTY
   2.1 The Receiving Party agrees to:
       (a) Hold the Confidential Information in strict confidence;
       (b) Not disclose the Confidential Information to any third party without
           prior written consent of the Disclosing Party;
       (c) Use the Confidential Information solely for the Purpose stated above;
       (d) Protect the Confidential Information using at least the same degree
           of care used to protect its own confidential information, but in no
           event less than reasonable care;
       (e) Immediately notify the Disclosing Party upon discovery of any
           unauthorized use or disclosure of the Confidential Information.

3. EXCLUSIONS
   This Agreement does not apply to information that:
   (a) Is or becomes publicly known through no breach of this Agreement;
   (b) Was rightfully known by the Receiving Party before receipt;
   (c) Is independently developed by the Receiving Party without use of
       the Confidential Information;
   (d) Is required to be disclosed by law, court order, or governmental authority,
       provided the Receiving Party gives prompt written notice to the Disclosing Party.

4. TERM
   4.1 This Agreement shall be effective as of the date first above written and
       shall continue for a period of {f.get('duration', '2 years')}.
   4.2 The obligations of confidentiality shall survive the termination of
       this Agreement for a period of 3 (three) years.

5. RETURN OF INFORMATION
   Upon termination of this Agreement or upon request, the Receiving Party
   shall promptly return or destroy all Confidential Information received,
   including all copies, notes, and summaries thereof.

6. INTELLECTUAL PROPERTY
   All Confidential Information remains the exclusive property of the Disclosing
   Party. Nothing in this Agreement grants any license or rights to the Receiving
   Party in or to the Confidential Information.

7. REMEDIES
   The Receiving Party acknowledges that any breach of this Agreement may cause
   irreparable harm to the Disclosing Party for which monetary damages may be
   inadequate, and that the Disclosing Party shall be entitled to seek equitable
   relief, including injunction and specific performance, in addition to all
   other remedies available under law.

8. GOVERNING LAW AND JURISDICTION
   8.1 This Agreement shall be governed by the Indian Contract Act, 1872,
       and the laws of India.
   8.2 Any disputes shall be subject to the exclusive jurisdiction of the
       courts in {f.get('city', '[City]')}.

9. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties concerning
   the subject matter hereof and supersedes all prior agreements, discussions,
   and understandings.

================================================================================
SIGNATURES
================================================================================

DISCLOSING PARTY:                           RECEIVING PARTY:

____________________________                ____________________________
{f.get('party1_name', '[Party 1]')}                         {f.get('party2_name', '[Party 2]')}
Date: ____________________                  Date: ____________________

Place: {f.get('city', '[City]')}
{DISCLAIMER}"""


def _employment_contract(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
EMPLOYMENT CONTRACT
================================================================================

This Employment Contract ("Contract") is executed on {date} at {f.get('city', '[City]')}.

BETWEEN:

EMPLOYER:
{f.get('employer_name', '[Employer Name]')}
(hereinafter referred to as "the Company" or "the Employer")

AND

EMPLOYEE:
{f.get('employee_name', '[Employee Name]')}
(hereinafter referred to as "the Employee")

================================================================================
TERMS OF EMPLOYMENT
================================================================================

1. DESIGNATION AND DUTIES
   1.1 The Employee is hereby appointed to the position of:
       {f.get('designation', '[Designation]')}
   1.2 The Employee shall perform all duties and responsibilities associated
       with this position and such other duties as may be assigned from time to time.
   1.3 The Employee shall report to the management of the Company.

2. DATE OF COMMENCEMENT
   The employment shall commence on {f.get('joining_date', '[Joining Date]')}.

3. PROBATION PERIOD
   The first six (6) months of employment shall be considered a probation period,
   during which either party may terminate this Contract by giving 15 days' notice.

4. COMPENSATION
   4.1 The Employee shall receive a monthly gross salary of Rs. {f.get('salary', '[Amount]')}
       (Rupees {f.get('salary', '[Amount]')} Only), subject to applicable TDS deductions.
   4.2 Salary shall be credited to the Employee's bank account on or before the
       last working day of each month.
   4.3 The salary structure shall include:
       - Basic Salary: 40% of CTC
       - HRA: 20% of Basic Salary
       - Special Allowance: Balance of CTC
   4.4 The Company shall make statutory deductions including PF (12% of Basic)
       and ESI where applicable.

5. WORKING HOURS
   5.1 Standard working hours shall be 9 hours per day, 5/6 days per week.
   5.2 The Employee may be required to work beyond normal hours during business
       exigencies without additional remuneration, unless otherwise agreed.

6. LEAVE ENTITLEMENT
   6.1 The Employee shall be entitled to:
       - Earned/Privilege Leave: 18 days per year
       - Casual Leave: 12 days per year
       - Sick Leave: 12 days per year
       - Public Holidays as per the Company's holiday calendar
   6.2 Leave is subject to prior approval and business requirements.

7. CONFIDENTIALITY
   7.1 The Employee shall maintain strict confidentiality of all trade secrets,
       business strategies, client information, and proprietary data.
   7.2 This obligation shall continue for 2 years after termination of employment.

8. NON-COMPETE
   8.1 During the term of employment, the Employee shall not engage in any
       activity that competes with the Company's business.
   8.2 Post-employment non-compete restrictions, if any, shall be subject to
       reasonableness as per Indian law.

9. INTELLECTUAL PROPERTY
   All work product, inventions, and developments created by the Employee during
   the course of employment shall be the exclusive property of the Company.

10. TERMINATION
    10.1 After probation, either party may terminate this Contract by providing
         one (1) month's written notice or payment of salary in lieu thereof.
    10.2 The Company may terminate employment without notice for gross misconduct,
         breach of contract, or conduct prejudicial to the Company's interests.
    10.3 Upon termination, the Employee shall return all company property and data.

11. GOVERNING LAW
    This Contract is governed by the Industrial Disputes Act, 1947, Shops &
    Establishments Act, and other applicable labour laws of India and the state
    of {f.get('city', '[City]')}.

================================================================================
ACKNOWLEDGEMENT AND SIGNATURES
================================================================================

The Employee confirms that they have read, understood, and agree to the terms
and conditions set forth in this Contract.

EMPLOYER:                                   EMPLOYEE:

____________________________                ____________________________
Authorized Signatory                        {f.get('employee_name', '[Employee Name]')}
{f.get('employer_name', '[Company Name]')}                      Date: ____________________
Date: ____________________

Place: {f.get('city', '[City]')}
{DISCLAIMER}"""


def _legal_notice(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
LEGAL NOTICE
================================================================================

Date: {date}
Place: {f.get('city', '[City]')}

TO,
{f.get('recipient_name', '[Recipient Name]')}
[Recipient's Address]

SUBJECT: {f.get('subject', '[Subject of Notice]')}

================================================================================

Dear Sir/Madam,

Under the instructions and on behalf of my client, {f.get('sender_name', '[Sender Name]')},
resident of {f.get('city', '[City]')}, I hereby serve upon you this Legal Notice as under:

1. BACKGROUND AND FACTS:

{f.get('details', '[Details of the matter, background, and relevant facts should be described here in detail.]')}

2. LEGAL POSITION:

The above-mentioned acts/omissions/conduct of the Noticee constitute a breach of
legal obligations and rights of my client under applicable laws including but not
limited to the Indian Contract Act, 1872, and other relevant statutes.

3. DEMAND:

In view of the above stated facts and circumstances, you are hereby called upon to:

{f.get('demand', '[Specific demand/action required from the recipient]')}

within FIFTEEN (15) DAYS from the receipt of this Notice, failing which my client
shall be constrained to initiate appropriate legal proceedings against you before
the competent court of law at {f.get('city', '[City]')}, seeking all legal remedies
available including damages, compensation, and costs.

4. RESERVATION OF RIGHTS:

Please note that all rights and remedies of my client are expressly reserved
and nothing in this notice shall be construed as a waiver of any rights.

Take notice accordingly and govern yourself.

Yours faithfully,

[Advocate's Signature]
Advocate & Legal Counsel
For and on behalf of: {f.get('sender_name', '[Sender Name]')}
Place: {f.get('city', '[City]')}
Date: {date}

NOTE: This notice is sent by registered post with acknowledgement due and
by electronic means.
{DISCLAIMER}"""


def _affidavit(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
AFFIDAVIT
================================================================================

I, {f.get('deponent_name', '[Deponent Name]')}, aged {f.get('age', '[Age]')} years,
residing at {f.get('address', '[Address]')}, do hereby solemnly affirm and declare
as under:

SUBJECT: {f.get('subject', '[Subject of Affidavit]')}

================================================================================
DECLARATION
================================================================================

1. I am the Deponent in the above-mentioned matter and as such am fully acquainted
   with the facts and circumstances of the case.

2. The facts stated herein are true and correct to the best of my knowledge,
   information, and belief and nothing material has been concealed therefrom.

3. {f.get('statements', '[Specific factual statements to be declared]')}

4. I make this Affidavit to state the facts truly and for the purposes of
   {f.get('subject', '[purpose]')} and for no other purpose.

5. I declare that the contents of this Affidavit are true and correct, and
   no part thereof is false, and nothing material has been concealed therefrom.

================================================================================
VERIFICATION
================================================================================

Verified at {f.get('city', '[City]')} on this {date}.

I, {f.get('deponent_name', '[Deponent Name]')}, the above-named Deponent, do hereby
verify that the contents of paragraphs 1 to 5 of this Affidavit are true and
correct to the best of my knowledge, information, and belief, and that nothing
material has been concealed therefrom.


____________________________
{f.get('deponent_name', '[Deponent Name]')}
DEPONENT

Solemnly affirmed and declared before me on {date} at {f.get('city', '[City]')}

____________________________
Notary Public / Oath Commissioner
Seal:
Registration No.:
Place: {f.get('city', '[City]')}
{DISCLAIMER}"""


def _power_of_attorney(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
POWER OF ATTORNEY
================================================================================

KNOW ALL MEN BY THESE PRESENTS that I/We,

PRINCIPAL (GRANTOR):
{f.get('grantor_name', '[Grantor Name]')}
(hereinafter referred to as "the Principal")

do hereby appoint, authorize, and constitute:

ATTORNEY-IN-FACT:
{f.get('attorney_name', '[Attorney Name]')}
(hereinafter referred to as "the Attorney")

as my/our true and lawful attorney-in-fact and agent, to act in my/our name,
place, and stead in the following matters:

================================================================================
PURPOSE AND SCOPE OF AUTHORITY
================================================================================

PURPOSE: {f.get('purpose', '[Specific purpose for granting Power of Attorney]')}

SCOPE OF AUTHORITY:
{f.get('scope', '[Detailed description of the powers being granted, e.g., sign documents, appear before authorities, etc.]')}

Specifically, the Attorney is authorized to:

1. Do, perform, and execute all acts, deeds, and things as may be necessary
   for the above stated purpose.
2. Sign, execute, acknowledge, and deliver all documents, agreements, deeds,
   and instruments as may be required.
3. Appear before all courts, tribunals, offices, and authorities on behalf
   of the Principal.
4. Receive payments, sign receipts, and give valid discharges.
5. Generally do all other acts, deeds, and things as may be necessary for
   the above purpose as fully and effectually as the Principal could do personally.

================================================================================
TERMS
================================================================================

1. This Power of Attorney shall remain in force until revoked by the Principal
   in writing.
2. The Principal hereby ratifies and confirms all acts done by the Attorney
   in good faith pursuant to this Power of Attorney.
3. Third parties may rely on this Power of Attorney until they receive written
   notice of its revocation.

IN WITNESS WHEREOF, the Principal has set their hand and seal on {date} at
{f.get('city', '[City]')}.

================================================================================
SIGNATURES
================================================================================

PRINCIPAL:

____________________________
{f.get('grantor_name', '[Grantor Name]')}
Date: {date}
Place: {f.get('city', '[City]')}

ACCEPTED BY ATTORNEY:

____________________________
{f.get('attorney_name', '[Attorney Name]')}
Date: ____________________

WITNESSES:

1. ____________________________             2. ____________________________
   Name: ____________________                 Name: ____________________
   Address: __________________                Address: __________________

NOTARIZED BY:
____________________________
Notary Public
Seal:
Registration No.:
{DISCLAIMER}"""


def _fir_complaint(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
APPLICATION FOR REGISTRATION OF FIR / POLICE COMPLAINT
================================================================================

Date: {date}

TO,
The Station House Officer (SHO)
[Name of Police Station]
{f.get('city', '[City]')}

================================================================================
COMPLAINT / FIRST INFORMATION REPORT
================================================================================

Subject: Complaint regarding [nature of offence] — request for registration of FIR

Respected Sir/Madam,

I, {f.get('complainant_name', '[Complainant Name]')}, submit this complaint as follows:

1. NAME OF COMPLAINANT:
   {f.get('complainant_name', '[Complainant Name]')}
   [Address of Complainant]
   Contact No.: [Phone Number]

2. NAME OF ACCUSED/SUSPECT:
   {f.get('accused_name', '[Name of accused / Unknown]')}
   [Address of Accused if known]

3. DATE AND TIME OF INCIDENT:
   {f.get('incident_date', '[Date of Incident]')}

4. PLACE OF OCCURRENCE:
   {f.get('location', '[Location / Address where incident occurred]')}
   Police Station Jurisdiction: [Police Station Name], {f.get('city', '[City]')}

5. DETAILS OF THE INCIDENT:
   (Complete narration of facts as known to the complainant)

   {f.get('incident_details', '[Provide complete details of the incident including sequence of events, persons involved, any witnesses, and any other relevant facts]')}

6. OFFENCES COMMITTED:
   Based on the above facts, the following offences appear to have been committed
   under the Indian Penal Code, 1860 (IPC) / Bharatiya Nyaya Sanhita, 2023 (BNS):
   [Applicable Sections — e.g., IPC Section 420 (Cheating), Section 379 (Theft), etc.]

7. WITNESSES (if any):
   (i) [Name and Address of Witness 1]
   (ii) [Name and Address of Witness 2]

8. PROPERTY INVOLVED / DOCUMENTS:
   [Mention any property stolen/damaged or documents involved]

9. PRAYER:
   In view of the above, I respectfully request your good office to:
   (a) Register an FIR against the accused under applicable sections of the IPC/BNS;
   (b) Investigate the matter thoroughly;
   (c) Take appropriate legal action against the accused.

I undertake that the above information is true and correct to the best of my
knowledge and belief. I am willing to cooperate in the investigation.

Yours faithfully,

____________________________
{f.get('complainant_name', '[Complainant Name]')}
Date: {date}
Place: {f.get('city', '[City]')}

--------------------------------------------------------------------------------
FOR POLICE USE ONLY:
FIR No.: ____________  Date: ____________  Time: ____________
Receiving Officer (Name & Badge No.): _______________________________
{DISCLAIMER}"""


def _consumer_complaint(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
COMPLAINT BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
================================================================================

Before the District Consumer Disputes Redressal Commission,
{f.get('city', '[City]')}

Consumer Complaint No.: ____________ / {datetime.now().year}

IN THE MATTER OF:
{f.get('complainant_name', '[Complainant Name]')}
[Address of Complainant]
                                                    ... COMPLAINANT

VERSUS

{f.get('company_name', '[Company / Service Provider Name]')}
[Address of Opposite Party]
                                                    ... OPPOSITE PARTY

================================================================================
COMPLAINT
================================================================================

The Complainant respectfully submits as follows:

1. PARTIES
   1.1 The Complainant, {f.get('complainant_name', '[Name]')}, is a consumer as defined
       under Section 2(7) of the Consumer Protection Act, 2019.
   1.2 The Opposite Party, {f.get('company_name', '[Company Name]')}, is engaged in the
       business of providing {f.get('product_service', '[product/service]')}.

2. CAUSE OF ACTION
   2.1 On {f.get('issue_date', '[Date]')}, the Complainant purchased/availed
       {f.get('product_service', '[product/service]')} from the Opposite Party.
   2.2 The details of the defect/deficiency are as follows:

       {f.get('complaint_details', '[Provide complete details of the complaint, including what was purchased, what went wrong, correspondence with company, and the loss/damage suffered]')}

3. LEGAL GROUNDS
   3.1 The acts and omissions of the Opposite Party constitute:
       (a) Deficiency in service under Section 2(11) of the Consumer Protection Act, 2019;
       (b) Unfair trade practice under Section 2(47) of the Act;
       (c) Sale of defective goods under Section 2(10) of the Act.

4. CAUSE OF ACTION AROSE
   The cause of action arose on {f.get('issue_date', '[date]')} and is continuing.
   The complaint is within the limitation period of 2 years under Section 69 of
   the Consumer Protection Act, 2019.

5. JURISDICTION
   This Commission has jurisdiction as the cause of action arose within its
   territorial jurisdiction and the claim amount falls within its pecuniary jurisdiction.

6. RELIEF SOUGHT
   In view of the foregoing, the Complainant humbly prays that this Commission
   may be pleased to:
   (a) Direct the Opposite Party to replace/refund the defective product/service;
   (b) Award compensation of Rs. [Amount] for mental agony and harassment;
   (c) Award costs of this complaint;
   (d) Pass any other order as this Commission may deem fit and just.

================================================================================
DECLARATION
================================================================================

I, {f.get('complainant_name', '[Name]')}, the above-named Complainant, do hereby
declare that the facts stated in this complaint are true and correct to the best
of my knowledge and belief.

____________________________
{f.get('complainant_name', '[Complainant Name]')}
Date: {date}
Place: {f.get('city', '[City]')}

VERIFICATION:
Verified at {f.get('city', '[City]')} on {date} that the facts stated above are
true and correct.

____________________________
Complainant
{DISCLAIMER}"""


def _rti_application(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
APPLICATION UNDER THE RIGHT TO INFORMATION ACT, 2005
================================================================================

Date: {date}

TO,
The Public Information Officer (PIO),
{f.get('authority_name', '[Name of Authority/Department]')},
{f.get('department', '[Department Name]')},
{f.get('city', '[City]')}

================================================================================
RTI APPLICATION
================================================================================

SUBJECT: Application seeking information under Section 6(1) of the Right to
Information Act, 2005

Respected Sir/Madam,

I, {f.get('applicant_name', '[Applicant Name]')}, residing at {f.get('address', '[Address]')},
hereby request you to provide the following information under the Right to
Information Act, 2005:

1. INFORMATION SOUGHT:

{f.get('information_sought', '[Describe exactly what information you are seeking. Be specific about the time period, documents, records, or data you need.]')}

2. FORMAT OF INFORMATION:
   Please provide the information in [hard copy / soft copy / both] format.

3. REASONS (Optional):
   The information is sought in public interest and for personal use.

4. PERSONAL DETAILS:
   Name: {f.get('applicant_name', '[Name]')}
   Address: {f.get('address', '[Address]')}
   Contact Number: [Phone Number]
   Email: [Email Address]

5. PAYMENT:
   An IPO / Court Fee Stamp / Demand Draft of Rs. 10/- (Rupees Ten Only) is
   enclosed herewith as the prescribed application fee.
   (Note: BPL card holders are exempt from fee — attach copy of BPL card)

6. REQUEST:
   (a) Please provide the above information within 30 days as required under
       Section 7(1) of the RTI Act, 2005.
   (b) If the information sought is not held by your office, please transfer
       this application to the concerned PIO under Section 6(3) and inform
       me accordingly.

Yours faithfully,

____________________________
{f.get('applicant_name', '[Applicant Name]')}
Date: {date}
Place: {f.get('city', '[City]')}

--------------------------------------------------------------------------------
ACKNOWLEDGEMENT (For Official Use)

Application No.: ____________  Date of Receipt: ____________
Name of PIO: ________________________  Signature: ____________
Note: Information shall be provided within 30 days. For matters affecting life
and liberty, within 48 hours (Section 7(1) RTI Act, 2005).
{DISCLAIMER}"""


def _will_testament(f: dict) -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""
LAST WILL AND TESTAMENT
================================================================================

I, {f.get('testator_name', '[Testator Name]')}, aged {f.get('age', '[Age]')} years,
residing at {f.get('address', '[Address]')}, being of sound and disposing mind,
memory, and understanding, and not acting under any duress, menace, fraud,
or undue influence of any person whatsoever, do hereby make, publish, and
declare this as my LAST WILL AND TESTAMENT, hereby revoking all former Wills
and Codicils made by me.

Date of Execution: {date}
Place: {f.get('city', '[City]')}

================================================================================
DECLARATIONS
================================================================================

1. PERSONAL PARTICULARS
   Full Name: {f.get('testator_name', '[Name]')}
   Age: {f.get('age', '[Age]')} years
   Permanent Address: {f.get('address', '[Address]')}
   Religion: [Religion]

2. EXECUTOR
   I hereby appoint {f.get('executor_name', '[Executor Name]')} as the sole Executor of
   this Will. In the event of the Executor being unable or unwilling to act, I appoint
   [Alternate Executor Name] as the Alternate Executor.

   The Executor shall have the full power and authority to:
   (a) Collect all assets and pay all debts and liabilities of my estate;
   (b) Administer and distribute my estate in accordance with this Will;
   (c) Take all legal steps necessary for the administration of my estate.

3. PAYMENT OF DEBTS AND EXPENSES
   I direct that all my just debts, funeral expenses, and costs of proving
   this Will shall be paid by my Executor as soon as possible after my death
   from my estate.

4. DISTRIBUTION OF ASSETS
   Subject to payment of debts and expenses, I bequeath my assets as follows:

   Beneficiaries: {f.get('beneficiaries', '[Names and relationship of beneficiaries]')}

   Distribution:
   {f.get('assets_distribution', '[Describe which assets go to which beneficiary. E.g., "The residential property at [address] to my son [Name]", "Fixed deposits to my daughter [Name]", etc.]')}

   Residuary Estate:
   All remaining assets not specifically disposed of above shall pass to
   {f.get('beneficiaries', '[Primary beneficiary]')}.

5. GUARDIAN FOR MINOR CHILDREN (if applicable)
   If any beneficiary is a minor at the time of my death, I appoint
   [Guardian Name] as the Guardian of such minor's share until they
   attain the age of 18 years.

6. SPECIFIC BEQUESTS
   [Any specific items of personal property or specific monetary amounts
   to specific individuals may be listed here]

================================================================================
REVOCATION
================================================================================

I hereby revoke all former Wills, Codicils, and Testamentary writings
previously made by me.

================================================================================
ATTESTATION AND SIGNATURES
================================================================================

IN WITNESS WHEREOF, I have hereunto set my hand to this, my Last Will and
Testament, written on this {date}, at {f.get('city', '[City]')}, declaring this
to be my act and deed.

____________________________
{f.get('testator_name', '[Testator Name]')}
TESTATOR

(Signed in the presence of the witnesses below, and each witness has
signed in the presence of the Testator and of each other)

WITNESSES:
(Note: Witnesses should not be beneficiaries under this Will)

1. Signature: ____________________________
   Full Name: ____________________________
   Address: ____________________________
   Date: ____________________________

2. Signature: ____________________________
   Full Name: ____________________________
   Address: ____________________________
   Date: ____________________________

================================================================================
IMPORTANT NOTES
================================================================================
- This Will should be registered at the Sub-Registrar's Office for enhanced
  legal validity (Section 18 of the Registration Act, 1908).
- Keep the original in a safe place and inform the Executor of its location.
- Review and update this Will periodically or after major life events.
{DISCLAIMER}"""


# ─── Template function map ────────────────────────────────────────────────────

_GENERATORS = {
    "rental_agreement": _rental_agreement,
    "nda": _nda,
    "employment_contract": _employment_contract,
    "legal_notice": _legal_notice,
    "affidavit": _affidavit,
    "poa": _power_of_attorney,
    "fir_complaint": _fir_complaint,
    "consumer_complaint": _consumer_complaint,
    "rti_application": _rti_application,
    "will_testament": _will_testament,
}


# ─── Custom prompt → best template match ─────────────────────────────────────

_CUSTOM_KEYWORDS = {
    "rental_agreement": ["rental", "rent", "lease", "tenant", "landlord", "flat", "house", "apartment"],
    "nda": ["nda", "non-disclosure", "confidentiality", "confidential", "secret"],
    "employment_contract": ["employment", "job", "hire", "salary", "employee", "designation", "work contract"],
    "legal_notice": ["legal notice", "notice", "demand", "warning letter"],
    "affidavit": ["affidavit", "sworn statement", "depose", "declaration", "notary"],
    "poa": ["power of attorney", "poa", "authorize", "attorney"],
    "fir_complaint": ["fir", "police complaint", "crime", "theft", "fraud", "report to police"],
    "consumer_complaint": ["consumer", "complaint", "defective", "refund", "product", "service complaint"],
    "rti_application": ["rti", "right to information", "information from government"],
    "will_testament": ["will", "testament", "inheritance", "bequeath", "estate", "death"],
}


def _detect_template_from_prompt(prompt: str) -> str | None:
    p = prompt.lower()
    best = None
    best_score = 0
    for tid, keywords in _CUSTOM_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in p)
        if score > best_score:
            best_score = score
            best = tid
    return best if best_score > 0 else None


def _extract_fields_from_prompt(prompt: str, template_id: str) -> dict:
    """Minimal field extraction from free-text custom prompts."""
    import re
    fields = {}

    # Try to extract common patterns
    name_patterns = re.findall(r'(?:between|by|for|named?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', prompt)
    amount_patterns = re.findall(r'(?:Rs\.?|₹)\s*([\d,]+)', prompt)
    date_patterns = re.findall(r'(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4}|\w+\s+\d{4})', prompt)
    city_patterns = re.findall(
        r'\b(Mumbai|Delhi|Bangalore|Bengaluru|Chennai|Hyderabad|Kolkata|Pune|Ahmedabad|Jaipur|Lucknow|Surat|Patna|Bhopal|Indore|Nagpur)\b',
        prompt, re.IGNORECASE
    )

    if name_patterns:
        fields["party1_name"] = name_patterns[0]
        fields["grantor_name"] = name_patterns[0]
        fields["sender_name"] = name_patterns[0]
        fields["landlord_name"] = name_patterns[0]
        fields["employer_name"] = name_patterns[0]
        fields["complainant_name"] = name_patterns[0]
        if len(name_patterns) > 1:
            fields["party2_name"] = name_patterns[1]
            fields["tenant_name"] = name_patterns[1]
            fields["employee_name"] = name_patterns[1]
            fields["recipient_name"] = name_patterns[1]
    if amount_patterns:
        fields["rent_amount"] = amount_patterns[0].replace(",", "")
        fields["salary"] = amount_patterns[0].replace(",", "")
    if date_patterns:
        fields["joining_date"] = date_patterns[0]
        fields["incident_date"] = date_patterns[0]
        fields["issue_date"] = date_patterns[0]
    if city_patterns:
        fields["city"] = city_patterns[0]

    fields["details"] = prompt
    fields["purpose"] = prompt[:200]
    fields["scope"] = prompt[:200]
    fields["information_sought"] = prompt[:300]
    fields["statements"] = prompt[:300]
    fields["incident_details"] = prompt[:300]
    fields["complaint_details"] = prompt[:300]
    fields["assets_distribution"] = prompt[:300]
    return fields


# ─── Public API ───────────────────────────────────────────────────────────────

def get_templates() -> list:
    return DOCUMENT_TEMPLATES


def generate_document(template_id: str, fields: dict, custom_prompt: str = None) -> dict:
    # Handle custom prompt
    if custom_prompt:
        detected_id = _detect_template_from_prompt(custom_prompt)
        if detected_id:
            extracted = _extract_fields_from_prompt(custom_prompt, detected_id)
            # Override with any fields explicitly provided
            extracted.update({k: v for k, v in fields.items() if v})
            template_id = detected_id
            fields = extracted
        else:
            # Unknown document type — return a generic legal letter
            fields = _extract_fields_from_prompt(custom_prompt, "legal_notice")
            fields["details"] = custom_prompt
            fields["subject"] = "Legal Document Request"
            template_id = "legal_notice"

    generator = _GENERATORS.get(template_id)
    if not generator:
        return {"error": f"Unknown template: {template_id}"}

    template_meta = next((t for t in DOCUMENT_TEMPLATES if t["id"] == template_id), {})

    try:
        content = generator(fields)
        return {
            "template_id": template_id,
            "template_name": template_meta.get("name", "Legal Document"),
            "content": content.strip(),
            "fields": fields,
        }
    except Exception as e:
        return {"error": f"Generation failed: {type(e).__name__}: {e}"}

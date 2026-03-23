from mcp.server.fastmcp import FastMCP
from typing import Literal
from datetime import date

mcp = FastMCP("BU Cover Letter Generator")

CHECKLIST = [
    "Cover letter is 1 page or less",
    "Name is at the top, bold, and clear",
    "Text is between sizes 10-12",
    "Margins are between 0.5-1 inch",
    "Header matches resume header",
    "Addressed to correct recipient",
    "Signed off with Sincerely",
    "Everything is in active voice",
    "Strong action verbs used",
    "Writing is clear and illustrative",
    "Writing is confident and professional",
    "200-350 words for main text",
    "Job title and company name included in body",
    "Shows genuine interest in company goals",
    "Skills match the employer requirements",
    "Does not repeat or summarize the resume",
    "Uses CAR method with specific metrics",
    "Shows accomplishments not just tasks",
    "Focuses on what candidate brings to company",
    "All dates and locations are accurate"
]

@mcp.tool()
def generate_cover_letter(
    job_description: str,
    company_name: str,
    your_name: str,
    contact_info: str,
    resume_text: str = "",

    # ENUM 1 — Recipient — NO DEFAULT, must ask user
    recipient_type: Literal[
        "Hiring Manager",
        "Recruiter",
        "I know the name — ask me for it",
        "Skip — default to Hiring Manager"
    ],

    # ENUM 1b — Salutation — NO DEFAULT
    recipient_salutation: Literal[
        "Mr.",
        "Ms.",
        "Skip — use full name, gender neutral"
    ],

    # ENUM 2 — Location — NO DEFAULT
    location_type: Literal[
        "I know the location — ask me for it",
        "Skip — leave blank"
    ],

    recipient_name: str = "",
    company_address: str = "",

) -> str:
    """
    Generate a cover letter following BU COM Career Services guidelines.

    WORKFLOW — follow this EXACTLY every single time, no exceptions:

    STEP 1: Check your memory for this user's name, contact info,
            and resume. If you already have all three, skip to STEP 2.

            If you are missing ANY of them:
            - Ask for their full name. Wait for answer.
            - Ask for their contact info in this format:
              phone | city | email | linkedin
              Wait for answer.
            - Say: "Please attach your resume as a PDF so I can
              tailor the letter to your experience."
              Wait for them to attach it.
            - Read the full text from the PDF.
            - Store name, contact info, and resume text in your memory.
            - Confirm: "Got it — I've saved your details and won't
              ask again."

    STEP 2: Ask these questions ONE BY ONE.
            Wait for each answer before asking the next.
            Do NOT call this tool until ALL three are answered.

            QUESTION 1 — ask exactly:
            "Who should I address this letter to?"
            Show these options:
            • Hiring Manager
            • Recruiter
            • I know the name — ask me for it
            • Skip — default to Hiring Manager

            If they choose "I know the name — ask me for it":
            Ask: "What is their full name?" Wait for answer.

            QUESTION 2 — ask only if name was chosen above:
            "What salutation should I use?"
            • Mr.
            • Ms.
            • Skip — use full name, gender neutral

            QUESTION 3 — ask exactly:
            "Do you have the company address or location?"
            • I know the location — ask me for it
            • Skip — leave blank

            If they choose "I know the location — ask me for it":
            Ask: "What is the address?" Wait for answer.

    STEP 3: Call this tool ONLY after ALL questions are answered
            and all required fields are filled.

    STEP 4: Each generation is COMPLETELY ISOLATED.
            Ignore any previous cover letters in this conversation.
            Never reference, improve, or build on previous output.
            Start from zero every single time.

    CRITICAL: ENUMs have no defaults intentionally.
    You MUST collect every answer from the user before calling this tool.
    Assuming defaults is a violation of this workflow.
    """

    # Resolve recipient
    if recipient_type in ["Skip — default to Hiring Manager", "Hiring Manager"]:
        greeting = "Dear Hiring Manager,"
        recipient_block_name = "Hiring Manager"
    elif recipient_type == "Recruiter":
        greeting = "Dear Recruiter,"
        recipient_block_name = "Recruiter"
    elif recipient_type == "I know the name — ask me for it" and recipient_name:
        recipient_block_name = recipient_name
        if recipient_salutation == "Mr.":
            greeting = f"Dear Mr. {recipient_name},"
        elif recipient_salutation == "Ms.":
            greeting = f"Dear Ms. {recipient_name},"
        else:
            greeting = f"Dear {recipient_name},"
    else:
        greeting = "Dear Hiring Manager,"
        recipient_block_name = "Hiring Manager"

    # Resolve location
    address_line = (
        company_address
        if location_type == "I know the location — ask me for it"
        and company_address
        else ""
    )

    # Today's date
    today = date.today().strftime("%B %d, %Y")

    prompt = f"""
CRITICAL ISOLATION INSTRUCTION: This is a completely fresh cover letter
generation. Ignore any previous cover letters in this conversation entirely.
Start from zero using only the inputs provided below. Do not reference,
improve, or build upon anything generated earlier in this conversation.

You are a BU COM Career Services advisor with 20 years of experience
helping students land jobs at top companies.

STRICT BU COM RULES:
- Total word count for all paragraphs combined: 200-350 words
- Use the CAR method (Context, Action, Results) with specific metrics
- Depth not breadth — pick 1-2 skills maximum and go deep
- Active voice only — no passive constructions
- Never summarize the resume — expand on it with stories
- Focus on what the candidate brings, never what they gain
- Extract ATS keywords from the job description naturally
- Opening must lead with a specific insight about THIS company or role
- Never start with "I am writing to apply"
- Closing must NOT start with "I look forward"

BANNED PHRASES — never use these under any circumstances:
- "resonates deeply with me"
- "fast-paced environment"
- "hardworking and dedicated"
- "strong work ethic"
- "team player"
- Any phrase that could appear unchanged in any other cover letter

OPENING PARAGRAPH RULES:
- First sentence must reference something specific about THIS company
  or THIS role — not generic praise
- Name the exact position title
- Mention 2-3 skills with a hint of evidence, not just claims

MIDDLE PARAGRAPH RULES:
- Start with the skill, never with "I"
- Follow CAR strictly:
  Context — what was the situation
  Action — exactly what YOU did, not the team
  Result — specific metric or measurable outcome
- If no direct metric exists, use a proxy — adoption rate, scale,
  efficiency gain, number of stakeholders, timeline

CLOSING PARAGRAPH RULES:
- Must NOT start with "I look forward"
- Reference something specific about the role or company
- Thank them without being sycophantic
- End with a confident but not arrogant invitation to connect

FORMAT OUTPUT EXACTLY LIKE THIS — no preamble, no explanation,
output the letter immediately:

---

**{your_name}**
{contact_info}

{today}

{recipient_block_name}
{address_line}

{greeting}

[opening paragraph]

[middle paragraph 1]

[middle paragraph 2 — omit if already at 300 words]

[closing paragraph]

Sincerely,

{your_name}

---

**BU COM Checklist:**
Go through every item and mark with ✅ or ❌:
{chr(10).join(f"- {item}" for item in CHECKLIST)}

CANDIDATE NAME: {your_name}
CONTACT INFO: {contact_info}
RESUME CONTENT:
{resume_text}
TARGET COMPANY: {company_name}
JOB DESCRIPTION:
{job_description}
"""

    return prompt


if __name__ == "__main__":
    mcp.run()
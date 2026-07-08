import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from dotenv import dotenv_values
from openai import OpenAI

from quotepilot_tools import run_business_workflow
from quote_outputs import generate_quote_pdf, oss_is_configured, upload_file_to_oss

APP_NAME = "QuotePilot AI"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
INQUIRIES_FILE = DATA_DIR / "inquiries.jsonl"
SAMPLE_FILE = DATA_DIR / "sample_inquiries.json"

cfg = dotenv_values(".env")
QWEN_API_KEY = cfg.get("QWEN_API_KEY", "") or os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = cfg.get("QWEN_BASE_URL", "") or os.getenv(
    "QWEN_BASE_URL",
    "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)
QWEN_MODEL = cfg.get("QWEN_MODEL", "") or os.getenv("QWEN_MODEL", "qwen-plus")

INTAKE_SYSTEM_PROMPT = """
You are QuotePilot Intake Agent.

You help a B2B company convert messy customer inquiries into structured quote-ready information.

Your job:
Read a customer inquiry and extract the important business information.

Rules:
- Return only valid JSON.
- Do not use markdown.
- Do not wrap the JSON in markdown fences.
- Do not invent missing information.
- If a field is unknown, use null.
- If something important is missing, add it to missing_fields.
- Estimate confidence from 0 to 1.
- If confidence is below 0.82, recommend clarification or human review.
- Do not calculate final prices. Pricing is handled by tools.
- Do not send emails.
- If the customer asks for urgent delivery, big discount, immediate sending, legal exceptions, unclear products, or unusually large quantity, add risk_flags.

Return JSON with exactly these keys:
{
  "customer_name": string or null,
  "company": string or null,
  "email": string or null,
  "intent": string,
  "products_requested": [
    {
      "description": string,
      "quantity": number or null
    }
  ],
  "delivery_location": string or null,
  "deadline": string or null,
  "budget": number or null,
  "currency": string or null,
  "special_terms": [string],
  "missing_fields": [string],
  "risk_flags": [string],
  "confidence": number,
  "recommended_next_action": string
}
"""


def get_qwen_client() -> OpenAI:
    if not QWEN_API_KEY:
        raise ValueError("QWEN_API_KEY is missing. Please check your .env file.")
    return OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)


def extract_json_from_text(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError("Could not parse JSON from Qwen response.")


def analyze_inquiry(raw_text: str) -> Dict[str, Any]:
    client = get_qwen_client()
    response = client.chat.completions.create(
        model=QWEN_MODEL,
        messages=[
            {"role": "system", "content": INTAKE_SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        temperature=0.1,
    )
    content = response.choices[0].message.content
    return extract_json_from_text(content)


def save_record(raw_text: str, extraction: Dict[str, Any], workflow: Dict[str, Any]) -> Dict[str, Any]:
    record = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": workflow.get("workflow_state", "UNKNOWN"),
        "raw_text": raw_text,
        "extraction": extraction,
        "workflow": workflow,
    }

    with INQUIRIES_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return record


def load_recent_records(limit: int = 5):
    if not INQUIRIES_FILE.exists():
        return []
    rows = INQUIRIES_FILE.read_text(encoding="utf-8").splitlines()
    records = []
    for row in rows[-limit:]:
        try:
            records.append(json.loads(row))
        except json.JSONDecodeError:
            continue
    return list(reversed(records))


def load_samples():
    if not SAMPLE_FILE.exists():
        return []
    return json.loads(SAMPLE_FILE.read_text(encoding="utf-8"))


def money(value: Any) -> str:
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"


def render_current_record(record: Dict[str, Any]):
    extraction = record.get("extraction", {})
    workflow = record.get("workflow", {})
    quote = workflow.get("quote", {})
    policy = workflow.get("policy", {})
    record_id = record.get("id", "current")

    st.success("Workflow loaded. Review the tabs below.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workflow State", workflow.get("workflow_state", "UNKNOWN"))
    col2.metric("Approval Required", "YES" if workflow.get("approval_required") else "NO")
    col3.metric("Quote Total", money(quote.get("total", 0)))
    col4.metric("Safe Auto-Send", "NO")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Qwen Extraction",
            "Tool Calls",
            "Quote Draft",
            "Policy Guard",
            "Human Approval",
            "PDF + OSS",
            "Audit Record",
        ]
    )

    with tab1:
        st.subheader("Structured data extracted by Qwen")
        st.json(extraction)

    with tab2:
        st.subheader("Business tools invoked by the agent")
        for index, call in enumerate(workflow.get("tool_calls", []), start=1):
            with st.expander(f"Tool {index}: {call.get('tool_name', 'unknown_tool')}", expanded=index <= 3):
                st.json(call)

    with tab3:
        st.subheader("Draft quote generated by pricing tool")
        if quote.get("line_items"):
            st.table(quote.get("line_items", []))
        else:
            st.warning("No quote line items were created because no catalog item was confidently matched.")

        st.write("**Subtotal:**", money(quote.get("subtotal", 0)))
        st.write("**Discount:**", money(quote.get("discount_amount", 0)))
        st.write("**Shipping estimate:**", money(quote.get("shipping_estimate", 0)))
        st.write("**Tax:**", money(quote.get("tax_amount", 0)))
        st.write("**Total:**", money(quote.get("total", 0)))
        st.info("This is a draft quote. It is not sent to the customer.")

    with tab4:
        st.subheader("Policy guard result")
        if policy.get("approval_required"):
            st.error("Human approval is required.")
        else:
            st.success("No approval issues detected, but external sending is still blocked for safety.")

        st.write("**Workflow state:**", policy.get("workflow_state"))
        st.write("**Safe to send without human:**", policy.get("safe_to_send_without_human"))

        st.write("**Approval reasons:**")
        reasons = policy.get("approval_reasons") or []
        if reasons:
            for reason in reasons:
                st.write("- " + str(reason))
        else:
            st.write("No approval reasons.")

        questions = policy.get("clarification_questions") or []
        if questions:
            st.write("**Clarification questions:**")
            for question in questions:
                st.write("- " + str(question))

    with tab5:
        st.subheader("Human-in-the-loop checkpoint")
        st.warning("QuotePilot never sends external emails without human approval.")

        decision_key = f"human_decision_{record_id}"
        decision = st.radio(
            "Human decision for this draft",
            ["Waiting for review", "Approve draft", "Request revision", "Reject draft"],
            key=decision_key,
        )

        if decision == "Approve draft":
            st.success("Human approved. You can now generate a PDF in the PDF + OSS tab.")
        elif decision == "Request revision":
            st.info("Human requested revision. In production, the workflow would return to the agent for changes.")
        elif decision == "Reject draft":
            st.error("Human rejected the draft. No customer response will be sent.")
        else:
            st.info("Waiting for a human reviewer.")

        st.write("**Email draft prepared by agent:**")
        st.text_area(
            "Draft email",
            value=(
                "Subject: "
                + workflow.get("email_draft", {}).get("subject", "")
                + "\n\n"
                + workflow.get("email_draft", {}).get("body", "")
            ),
            height=260,
            key=f"email_draft_{record_id}",
        )

    with tab6:
        st.subheader("PDF generation and Alibaba OSS upload")

        decision = st.session_state.get(f"human_decision_{record_id}", "Waiting for review")
        if decision != "Approve draft":
            st.warning("Select `Approve draft` in the Human Approval tab before generating the quote PDF.")
        else:
            st.success("Human approval detected. PDF generation is enabled.")

            if st.button("Generate approved quote PDF", key=f"generate_pdf_{record_id}"):
                pdf_result = generate_quote_pdf(record)
                st.session_state[f"pdf_result_{record_id}"] = pdf_result

            pdf_result = st.session_state.get(f"pdf_result_{record_id}")
            if pdf_result:
                st.success("PDF generated successfully.")
                st.json(pdf_result)

                file_path = pdf_result["file_path"]
                with open(file_path, "rb") as pdf_file:
                    st.download_button(
                        "Download quote PDF",
                        data=pdf_file,
                        file_name=pdf_result["file_name"],
                        mime="application/pdf",
                        key=f"download_pdf_{record_id}",
                    )

                if oss_is_configured():
                    st.info("Alibaba OSS configuration detected.")
                    if st.button("Upload PDF to Alibaba OSS", key=f"upload_oss_{record_id}"):
                        oss_result = upload_file_to_oss(file_path)
                        st.session_state[f"oss_result_{record_id}"] = oss_result

                    oss_result = st.session_state.get(f"oss_result_{record_id}")
                    if oss_result:
                        if oss_result.get("oss_uploaded"):
                            st.success("PDF uploaded to Alibaba OSS.")
                        else:
                            st.error("OSS upload did not complete.")
                        st.json(oss_result)
                else:
                    st.warning("Alibaba OSS is not configured yet. PDF download still works. Configure OSS variables in `.env` to enable upload.")

    with tab7:
        st.subheader("Audit events")
        st.json(workflow.get("audit_events", []))
        st.download_button(
            "Download full workflow JSON",
            data=json.dumps(record, indent=2),
            file_name=f"quotepilot_day3_record_{record_id}.json",
            mime="application/json",
            key=f"download_json_{record_id}",
        )


st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide")

if "current_record" not in st.session_state:
    st.session_state["current_record"] = None

st.title("🤖 QuotePilot AI")
st.caption("Track 4 Autopilot Agent — Qwen workflow automation with human approval, PDF output, and Alibaba OSS")

with st.sidebar:
    st.header("System Status")
    st.write("**App:** Running")
    st.write(f"**Model:** `{QWEN_MODEL}`")
    st.write(f"**Base URL:** `{QWEN_BASE_URL}`")
    if QWEN_API_KEY:
        st.success("Qwen API key detected")
    else:
        st.error("Qwen API key missing")

    st.divider()
    st.header("Track 4 Capabilities")
    st.write("✅ Qwen extraction")
    st.write("✅ Business tools")
    st.write("✅ Human approval checkpoint")
    st.write("✅ Human-approved quote PDF generation")
    if oss_is_configured():
        st.success("Alibaba OSS configured")
    else:
        st.warning("Alibaba OSS not configured")

st.subheader("1. Paste a customer inquiry")

samples = load_samples()
sample_names = ["Custom input"] + [sample["name"] for sample in samples]
selected_sample = st.selectbox("Choose sample or custom input", sample_names)

if selected_sample == "Custom input":
    default_text = ""
else:
    default_text = next(sample["text"] for sample in samples if sample["name"] == selected_sample)

raw_text = st.text_area(
    "Customer message",
    value=default_text,
    height=180,
    placeholder="Paste a customer email or message here...",
)

analyze_button = st.button("Analyze with Qwen + Run Business Tools", type="primary")

if analyze_button:
    if not raw_text.strip():
        st.warning("Please paste a customer inquiry first.")
    else:
        with st.spinner("Qwen is extracting details, then tools are running..."):
            try:
                extraction = analyze_inquiry(raw_text)
                workflow = run_business_workflow(extraction)
                record = save_record(raw_text, extraction, workflow)
                st.session_state["current_record"] = record
                st.success("Workflow completed and saved.")
            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)

if st.session_state.get("current_record"):
    render_current_record(st.session_state["current_record"])

st.divider()
st.subheader("Recent saved workflows")
recent_records = load_recent_records()

if not recent_records:
    st.write("No saved workflows yet.")
else:
    for item in recent_records:
        with st.expander(f"{item['created_at']} — {item['status']}"):
            st.write("**Raw inquiry:**")
            st.write(item.get("raw_text", ""))
            st.write("**Workflow state:**", item.get("workflow", {}).get("workflow_state"))
            st.write("**Quote total:**", money(item.get("workflow", {}).get("quote", {}).get("total", 0)))
            st.write("**Approval required:**", item.get("workflow", {}).get("approval_required"))
            if st.button("Load this workflow", key=f"load_{item['id']}"):
                st.session_state["current_record"] = item
                st.rerun()

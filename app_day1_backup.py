import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# -----------------------------
# Basic setup
# -----------------------------
load_dotenv()

APP_NAME = "QuotePilot AI"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
INQUIRIES_FILE = DATA_DIR / "inquiries.jsonl"
SAMPLE_FILE = DATA_DIR / "sample_inquiries.json"

QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = os.getenv(
    "QWEN_BASE_URL",
    "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")


# -----------------------------
# Prompt
# -----------------------------
INTAKE_SYSTEM_PROMPT = """
You are QuotePilot Intake Agent.

You help a B2B company convert messy customer inquiries into structured quote-ready information.

Your job:
Read a customer inquiry and extract the important business information.

Rules:
- Return only valid JSON.
- Do not use markdown.
- Do not wrap the JSON in triple backticks.
- Do not invent missing information.
- If a field is unknown, use null.
- If something important is missing, add it to missing_fields.
- Estimate confidence from 0 to 1.
- If confidence is below 0.82, recommend clarification or human review.
- Do not calculate final prices yet.
- Do not send emails.
- If the customer asks for urgent delivery, big discount, immediate sending, legal exceptions, or unclear products, add risk_flags.

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


# -----------------------------
# Helper functions
# -----------------------------
def get_qwen_client() -> OpenAI:
    if not QWEN_API_KEY:
        raise ValueError("QWEN_API_KEY is missing. Please create a .env file first.")

    return OpenAI(
        api_key=QWEN_API_KEY,
        base_url=QWEN_BASE_URL,
    )


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """Parse JSON even if the model accidentally adds extra text."""
    cleaned = text.strip()

    # Remove markdown fences if present
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to find the first JSON object in the text
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


def save_inquiry(raw_text: str, extraction: Dict[str, Any]) -> Dict[str, Any]:
    record = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "EXTRACTED",
        "raw_text": raw_text,
        "extraction": extraction,
        "audit_events": [
            {
                "event": "INQUIRY_RECEIVED",
                "message": "Customer inquiry was submitted.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            {
                "event": "QWEN_EXTRACTION_COMPLETED",
                "message": "Qwen extracted structured quote information.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ],
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


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 QuotePilot AI")
st.caption("Track 4 Autopilot Agent — Qwen-powered business workflow automation")

with st.sidebar:
    st.header("System Status")
    st.write("**App:** Running")
    st.write(f"**Model:** `{QWEN_MODEL}`")
    st.write(f"**Base URL:** `{QWEN_BASE_URL}`")

    if QWEN_API_KEY:
        st.success("Qwen API key detected")
    else:
        st.error("Qwen API key missing")
        st.info("Create a `.env` file with QWEN_API_KEY before testing.")

    st.divider()
    st.write("**Day 1 Goal:**")
    st.write("Paste inquiry → Qwen extracts JSON → Save audit record")

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

analyze_button = st.button("Analyze with Qwen", type="primary")

if analyze_button:
    if not raw_text.strip():
        st.warning("Please paste a customer inquiry first.")
    else:
        with st.spinner("Qwen is reading the inquiry..."):
            try:
                extraction = analyze_inquiry(raw_text)
                record = save_inquiry(raw_text, extraction)

                st.success("Qwen extraction completed and saved.")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("2. Structured extraction")
                    st.json(extraction)

                with col2:
                    st.subheader("3. Workflow decision")
                    st.write("**Status:** EXTRACTED")
                    st.write("**Recommended next action:**")
                    st.info(extraction.get("recommended_next_action", "No recommendation found."))

                    risk_flags = extraction.get("risk_flags", [])
                    missing_fields = extraction.get("missing_fields", [])
                    confidence = extraction.get("confidence", None)

                    st.write("**Confidence:**", confidence)

                    if missing_fields:
                        st.warning("Missing fields: " + ", ".join(missing_fields))
                    else:
                        st.success("No major missing fields detected.")

                    if risk_flags:
                        st.error("Risk flags: " + ", ".join(risk_flags))
                    else:
                        st.success("No major risk flags detected.")

                st.subheader("4. Audit record")
                st.json(record["audit_events"])

                st.download_button(
                    "Download extraction JSON",
                    data=json.dumps(record, indent=2),
                    file_name=f"quotepilot_record_{record['id']}.json",
                    mime="application/json",
                )

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)

st.divider()
st.subheader("Recent saved inquiries")
recent_records = load_recent_records()

if not recent_records:
    st.write("No saved inquiries yet.")
else:
    for item in recent_records:
        with st.expander(f"{item['created_at']} — {item['status']}"):
            st.write("**Raw inquiry:**")
            st.write(item["raw_text"])
            st.write("**Extraction:**")
            st.json(item["extraction"])

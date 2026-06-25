import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path("data")
CATALOG_FILE = DATA_DIR / "catalog.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit_event(event: str, message: str, details: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "event": event,
        "message": message,
        "details": details or {},
        "timestamp": utc_now(),
    }


def load_catalog() -> List[Dict[str, Any]]:
    if not CATALOG_FILE.exists():
        return []
    return json.loads(CATALOG_FILE.read_text(encoding="utf-8"))


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def lookup_catalog(product_description: str) -> Dict[str, Any]:
    catalog = load_catalog()
    query_tokens = _tokens(product_description)

    best_item = None
    best_score = 0.0

    for item in catalog:
        searchable = " ".join(
            [
                item.get("sku", ""),
                item.get("name", ""),
                item.get("description", ""),
                " ".join(item.get("aliases", [])),
            ]
        )
        item_tokens = _tokens(searchable)
        if not query_tokens or not item_tokens:
            score = 0.0
        else:
            score = len(query_tokens & item_tokens) / max(1, len(query_tokens))

        if score > best_score:
            best_score = score
            best_item = item

    matched = best_item is not None and best_score >= 0.20

    return {
        "tool_name": "lookup_catalog",
        "input": {"product_description": product_description},
        "matched": matched,
        "score": round(best_score, 2),
        "match": best_item if matched else None,
    }


def check_inventory(sku: str, quantity: int | None) -> Dict[str, Any]:
    catalog = load_catalog()
    quantity = int(quantity or 1)

    product = next((item for item in catalog if item.get("sku") == sku), None)
    if not product:
        return {
            "tool_name": "check_inventory",
            "input": {"sku": sku, "quantity": quantity},
            "found": False,
            "available": False,
            "stock": 0,
            "requested": quantity,
        }

    stock = int(product.get("stock", 0))
    return {
        "tool_name": "check_inventory",
        "input": {"sku": sku, "quantity": quantity},
        "found": True,
        "available": stock >= quantity,
        "stock": stock,
        "requested": quantity,
        "lead_time_days": product.get("lead_time_days"),
    }


def estimate_shipping(delivery_location: str | None, subtotal: float) -> float:
    if not delivery_location:
        return 0.0

    location = delivery_location.lower()
    base = 250.0

    if any(word in location for word in ["texas", "austin", "dallas", "houston"]):
        base = 180.0
    elif any(word in location for word in ["california", "new york", "florida"]):
        base = 320.0
    elif any(word in location for word in ["ghana", "nigeria", "kenya", "india", "uk", "canada"]):
        base = 650.0

    if subtotal > 10000:
        base += 250.0

    return base


def calculate_quote(items: List[Dict[str, Any]], delivery_location: str | None) -> Dict[str, Any]:
    line_items = []
    subtotal = 0.0

    for item in items:
        product = item["catalog_match"]
        quantity = int(item.get("quantity") or 1)
        unit_price = float(product.get("unit_price", 0))
        line_total = quantity * unit_price
        subtotal += line_total
        line_items.append(
            {
                "sku": product.get("sku"),
                "name": product.get("name"),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": round(line_total, 2),
                "currency": product.get("currency", "USD"),
            }
        )

    discount_rate = 0.05 if subtotal >= 5000 else 0.0
    discount_amount = subtotal * discount_rate
    shipping = estimate_shipping(delivery_location, subtotal)
    taxable_amount = max(0.0, subtotal - discount_amount) + shipping
    tax_rate = 0.08 if delivery_location else 0.0
    tax_amount = taxable_amount * tax_rate
    total = taxable_amount + tax_amount

    return {
        "tool_name": "calculate_quote",
        "input": {"delivery_location": delivery_location, "item_count": len(items)},
        "currency": "USD",
        "line_items": line_items,
        "subtotal": round(subtotal, 2),
        "discount_rate": discount_rate,
        "discount_amount": round(discount_amount, 2),
        "shipping_estimate": round(shipping, 2),
        "tax_rate": tax_rate,
        "tax_amount": round(tax_amount, 2),
        "total": round(total, 2),
        "quote_valid_days": 14,
    }


def policy_guard(extraction: Dict[str, Any], quote: Dict[str, Any], tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    approval_reasons = []
    clarification_questions = []

    missing_fields = extraction.get("missing_fields") or []
    risk_flags = extraction.get("risk_flags") or []

    try:
        confidence = float(extraction.get("confidence") or 0)
    except (TypeError, ValueError):
        confidence = 0.0

    if missing_fields:
        approval_reasons.append("Some inquiry fields are missing and should be reviewed.")
        critical_fields = {"products_requested", "product", "product_description", "quantity", "delivery_location"}
        for field in missing_fields:
            if str(field) in critical_fields:
                clarification_questions.append(f"Please provide {str(field).replace('_', ' ')}.")

    if confidence < 0.82:
        approval_reasons.append("Qwen extraction confidence is below 0.82.")

    if risk_flags:
        approval_reasons.append("Qwen detected risk flags: " + ", ".join(map(str, risk_flags)))

    total = float(quote.get("total") or 0)
    if total > 5000:
        approval_reasons.append("Quote total is above $5,000.")

    if quote.get("discount_rate", 0) > 0.10:
        approval_reasons.append("Discount is above 10%.")

    for call in tool_calls:
        if call.get("tool_name") == "check_inventory" and not call.get("available"):
            approval_reasons.append(
                f"Inventory issue for {call.get('input', {}).get('sku')}: requested {call.get('requested')} but stock is {call.get('stock')}."
            )

    if not quote.get("line_items"):
        approval_reasons.append("No catalog product was confidently matched.")
        clarification_questions.append("Please confirm the exact product or SKU requested.")

    approval_reasons.append("External customer response must be approved by a human before sending.")

    if clarification_questions:
        workflow_state = "NEEDS_CLARIFICATION"
    elif approval_reasons:
        workflow_state = "NEEDS_HUMAN_APPROVAL"
    else:
        workflow_state = "QUOTE_DRAFTED"

    return {
        "tool_name": "policy_guard",
        "workflow_state": workflow_state,
        "approval_required": bool(approval_reasons),
        "approval_reasons": approval_reasons,
        "clarification_questions": clarification_questions,
        "safe_to_send_without_human": False,
    }


def generate_email_draft(extraction: Dict[str, Any], quote: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    customer_name = extraction.get("customer_name") or "there"
    company = extraction.get("company") or "your organization"

    if policy.get("clarification_questions"):
        body_lines = [
            f"Hello {customer_name},",
            "",
            "Thank you for your inquiry. Before we can finalize a quote, please confirm the following:",
        ]
        for question in policy["clarification_questions"]:
            body_lines.append(f"- {question}")
        body_lines.extend(
            [
                "",
                "Once we receive this information, we can prepare a more accurate quote.",
                "",
                "Best regards,",
                "QuotePilot AI Draft",
            ]
        )
        subject = "Clarification needed for your quote request"
    else:
        total = quote.get("total", 0)
        currency = quote.get("currency", "USD")
        body_lines = [
            f"Hello {customer_name},",
            "",
            f"Thank you for contacting us on behalf of {company}.",
            f"We prepared a draft quote with an estimated total of {currency} {total}.",
            "",
            "This quote is valid for 14 days and is currently marked as DRAFT pending human approval.",
            "",
            "Best regards,",
            "QuotePilot AI Draft",
        ]
        subject = "Draft quote for your request"

    return {
        "tool_name": "prepare_email_draft",
        "subject": subject,
        "body": "\n".join(body_lines),
        "send_status": "DRAFT_ONLY_HUMAN_APPROVAL_REQUIRED",
    }


def run_business_workflow(extraction: Dict[str, Any]) -> Dict[str, Any]:
    tool_calls: List[Dict[str, Any]] = []
    quote_items: List[Dict[str, Any]] = []

    products_requested = extraction.get("products_requested") or []

    for requested in products_requested:
        description = requested.get("description", "") if isinstance(requested, dict) else str(requested)
        quantity = requested.get("quantity") if isinstance(requested, dict) else 1
        quantity = int(quantity or 1)

        catalog_result = lookup_catalog(description)
        tool_calls.append(catalog_result)

        if catalog_result.get("matched") and catalog_result.get("match"):
            sku = catalog_result["match"].get("sku")
            inventory_result = check_inventory(sku, quantity)
            tool_calls.append(inventory_result)
            quote_items.append(
                {
                    "catalog_match": catalog_result["match"],
                    "quantity": quantity,
                    "inventory": inventory_result,
                }
            )

    quote = calculate_quote(quote_items, extraction.get("delivery_location"))
    tool_calls.append(quote)

    policy = policy_guard(extraction, quote, tool_calls)
    tool_calls.append(policy)

    email_draft = generate_email_draft(extraction, quote, policy)
    tool_calls.append(email_draft)

    audit_events = [
        audit_event("INQUIRY_EXTRACTED", "Qwen extracted structured inquiry data."),
        audit_event("CATALOG_LOOKUP_COMPLETED", "Catalog lookup tool completed."),
        audit_event("INVENTORY_CHECK_COMPLETED", "Inventory check tool completed."),
        audit_event("QUOTE_CALCULATED", "Pricing tool created a draft quote."),
        audit_event("POLICY_GUARD_COMPLETED", "Policy guard evaluated risk and approval rules."),
        audit_event("EMAIL_DRAFT_PREPARED", "Customer response draft prepared but not sent."),
    ]

    return {
        "workflow_state": policy.get("workflow_state"),
        "approval_required": policy.get("approval_required"),
        "safe_to_send_without_human": False,
        "quote": quote,
        "policy": policy,
        "email_draft": email_draft,
        "tool_calls": tool_calls,
        "audit_events": audit_events,
    }

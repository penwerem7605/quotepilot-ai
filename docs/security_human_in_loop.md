# Security and Human-in-the-Loop Design

## Core safety rule

QuotePilot AI never sends a customer-facing email without human approval.

## Why human approval is required

Business quoting can involve:

- Wrong prices
- Wrong stock assumptions
- Unclear customer requirements
- Delivery risks
- High discounts
- Large order values
- Legal or payment exceptions

For this reason, QuotePilot uses AI for reasoning and drafting, but keeps humans in control of risky actions.

## Human approval triggers

QuotePilot requires approval when:

- Qwen extraction confidence is low.
- Required inquiry fields are missing.
- Quote value is high.
- Customer requests urgent delivery.
- Customer requests large discounts.
- Inventory is insufficient.
- The system is preparing external communication.

## Secret handling

Secrets must stay in `.env` or deployment environment variables.

Never commit:

- Qwen API key
- Alibaba AccessKey ID/Secret
- `.env`
- Identity documents
- Payment information

## Model/tool separation

Qwen extracts and reasons over the inquiry.

Deterministic tools handle:

- Catalog matching
- Inventory checks
- Pricing
- Policy decisions
- PDF generation

This prevents the model from inventing prices or stock levels.

## Current cloud status

Qwen Cloud API usage is active. Alibaba OSS upload code is implemented but live OSS testing is pending Alibaba account verification review.

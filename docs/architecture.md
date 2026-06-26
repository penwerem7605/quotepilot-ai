# QuotePilot AI Architecture

## Overview

QuotePilot AI is a Qwen-powered Autopilot Agent that automates the RFQ-to-Quote workflow for B2B customer inquiries.

It combines:

- Qwen Cloud for language understanding.
- Deterministic tools for business operations.
- Human approval checkpoints for safe automation.
- PDF generation for business-ready outputs.
- Alibaba OSS upload support for cloud storage once credentials are available.

## Architecture diagram

~~~mermaid
flowchart TD
    A[Customer Inquiry] --> B[Streamlit Web App]
    B --> C[Qwen Cloud Extraction]
    C --> D[Structured Inquiry JSON]
    D --> E[Autopilot Workflow]
    E --> F[Catalog Lookup Tool]
    E --> G[Inventory Check Tool]
    E --> H[Pricing Calculator]
    E --> I[Policy Guard]
    I --> J{Human Approval Required?}
    J -->|Yes| K[Human Approval Checkpoint]
    J -->|No but external action| K
    K --> L[Email Draft - Not Sent]
    K --> M[Quote PDF Generator]
    M --> N[Local PDF Download]
    M -. pending credentials .-> O[Alibaba Cloud OSS Upload]
    E --> P[Audit Record]
~~~

## Main files

| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface and workflow orchestration |
| `quotepilot_tools.py` | Catalog, inventory, pricing, policy guard, email draft tools |
| `quote_outputs.py` | PDF generation and Alibaba OSS upload support |
| `data/catalog.json` | Demo product catalog |
| `data/evaluation_cases.json` | Evaluation test cases |
| `.env.example` | Safe environment variable template |

## Workflow states

QuotePilot can produce states such as:

- `NEEDS_CLARIFICATION`
- `NEEDS_HUMAN_APPROVAL`
- `QUOTE_DRAFTED`

## Production-readiness choices

- API keys are kept out of GitHub.
- Prices and stock are handled by tools, not invented by the model.
- Risky actions trigger human approval.
- PDF generation happens only after human approval.
- External email sending is disabled in the hackathon demo.
- Alibaba OSS upload is implemented but gated by credentials.

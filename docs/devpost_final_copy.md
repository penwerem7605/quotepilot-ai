# Devpost Final Copy — QuotePilot AI

## Project name

QuotePilot AI

## Track

Track 4: Autopilot Agent

## Tagline

A Qwen-powered Autopilot Agent that turns messy B2B customer inquiries into safe, human-approved quote PDFs.

## Inspiration

Businesses often receive messy quote requests through email or chat. A simple customer message can require several manual steps: understand the request, identify products, check inventory, calculate pricing, review risk, and prepare a reply. QuotePilot AI was built to automate this workflow while keeping humans in control of risky customer-facing actions.

## What it does

QuotePilot AI automates the RFQ-to-Quote workflow:

- Reads messy customer inquiries.
- Uses Qwen Cloud to extract structured quote requirements.
- Looks up products in a catalog.
- Checks inventory.
- Calculates draft pricing.
- Applies policy and safety rules.
- Requires human approval before risky actions.
- Prepares an email draft without sending automatically.
- Generates a downloadable quote PDF after human approval.

## How we built it

QuotePilot AI was built with:

- Qwen Cloud for AI-powered inquiry understanding.
- Streamlit for the web dashboard.
- Python tool modules for catalog lookup, inventory checks, pricing, and policy guard logic.
- ReportLab for human-approved quote PDF generation.
- Alibaba Cloud OSS SDK support through `oss2` for cloud quote storage once account verification completes.
- GitHub Codespaces for cloud development from a Samsung Galaxy Tab S8+.

## Challenges we ran into

The project was built entirely from a tablet using cloud tools, which required a careful beginner-friendly workflow. We also focused on safe automation: the system should not invent stock, prices, or send customer emails without approval. Alibaba Cloud OSS live testing and deployment proof are pending account verification review, so the app currently falls back to local PDF generation and download while OSS support remains implemented in code.

## Accomplishments we are proud of

- Built a working Qwen-powered Autopilot Agent workflow.
- Implemented deterministic business tools instead of relying on the model to invent prices or stock.
- Added human-in-the-loop approval for safety.
- Generated quote PDFs after approval.
- Created strong documentation, evaluation cases, architecture docs, and deployment readiness files.

## What we learned

We learned that practical AI agents need more than a model. They need tools, policies, audit trails, human approval, and safe deployment practices. Qwen is powerful for understanding messy language, while deterministic Python tools keep business logic reliable.

## What's next

- Complete Alibaba Cloud OSS live upload after account verification.
- Deploy QuotePilot AI to Alibaba Cloud ECS or Simple Application Server.
- Add CRM integrations.
- Add approved email sending.
- Add more product catalogs and evaluation metrics.

# Devpost Submission Draft — QuotePilot AI

## Project name

QuotePilot AI

## Track

Track 4: Autopilot Agent

## Short description

QuotePilot AI is a Qwen-powered Autopilot Agent that automates the B2B RFQ-to-Quote workflow from messy customer inquiry to structured extraction, tool-based pricing, human approval, and quote PDF generation.

## Inspiration

Small businesses often receive vague customer quote requests by email or chat. Turning those messages into accurate quotes requires reading the request, checking products, checking stock, calculating price, reviewing risk, and drafting a response. This is repetitive but too risky to fully automate without safeguards. QuotePilot AI was built to show how Qwen-powered agents can automate the workflow while keeping humans in control.

## What it does

QuotePilot AI:

- Reads messy customer inquiries.
- Uses Qwen Cloud to extract structured quote requirements.
- Looks up products in a catalog.
- Checks inventory.
- Calculates draft quotes.
- Applies safety and policy rules.
- Requires human approval for risky or customer-facing actions.
- Generates downloadable quote PDFs.
- Includes Alibaba OSS upload support pending live cloud activation.

## How we built it

- Streamlit for the web interface.
- Qwen Cloud via OpenAI-compatible API for inquiry understanding.
- Python tool functions for catalog lookup, inventory checks, pricing, policy guard, and email draft generation.
- ReportLab for quote PDF generation.
- Alibaba Cloud OSS SDK support through `oss2` for future/upload-ready quote storage.
- GitHub Codespaces for tablet-only cloud development.

## Challenges

- Building entirely from a Samsung Galaxy Tab S8+ using cloud development tools.
- Keeping secrets safe while working from a browser-based environment.
- Designing safe automation that does not hallucinate prices or send emails without approval.
- Alibaba Cloud OSS live testing is pending account verification review, so the app currently falls back to local PDF generation and download.

## Accomplishments

- Built a working Qwen-powered workflow app from tablet-only development.
- Implemented end-to-end inquiry extraction, business tool orchestration, pricing, risk checks, human approval, and PDF generation.
- Created a safety-first Autopilot Agent that avoids unsafe auto-send behavior.
- Prepared deployment files and Alibaba OSS integration code for cloud deployment.

## What we learned

- AI agents are strongest when paired with deterministic tools.
- Human-in-the-loop checkpoints are essential for real business workflows.
- Production-readiness includes error handling, audit records, safe secrets, documentation, and deployment planning.

## What’s next

- Complete Alibaba Cloud OSS live upload after account verification.
- Deploy QuotePilot AI to Alibaba Cloud ECS or Simple Application Server.
- Add CRM integration.
- Add email provider integration after approval.
- Add richer product catalogs and quote templates.
- Add automated evaluation metrics.

## Links to add before final submission

- GitHub repo: [add link]
- Demo video: [add link]
- Alibaba Cloud deployment proof: [add link]
- Architecture diagram: `docs/architecture.md`

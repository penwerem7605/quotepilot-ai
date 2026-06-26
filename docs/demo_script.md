# QuotePilot AI Demo Video Script

Target length: about 3 minutes.

## 0:00 — Problem

Businesses lose time manually turning messy customer inquiries into accurate quotes. Manual quoting is slow, error-prone, and risky when discounts, inventory, or delivery deadlines are involved.

## 0:20 — Solution

QuotePilot AI is a Qwen-powered Autopilot Agent that automates the RFQ-to-Quote workflow. It reads customer inquiries, extracts structured requirements, invokes business tools, calculates draft quotes, and pauses for human approval before customer-facing actions.

## 0:45 — Architecture

Show architecture diagram.

Explain:

- Qwen Cloud extracts inquiry data.
- Business tools check catalog, inventory, pricing, and policies.
- Human approval protects risky workflows.
- PDF generation creates business-ready quote documents.

## 1:15 — Clean inquiry demo

Paste clean inquiry:

“Hi, this is Ada from BrightPath Schools. We need 3 solar classroom kits delivered to Austin, Texas by July 10. Please send a quote in USD.”

Show:

- Qwen extraction
- Tool calls
- Quote draft
- Human approval
- PDF generation

## 2:00 — Ambiguous inquiry demo

Use:

“Hello, we need some solar kits soon. How much will it cost?”

Show:

- Missing quantity
- Missing location
- Clarification needed
- No hallucinated final quote

## 2:25 — Risky inquiry demo

Use:

“We need 20 solar classroom kits delivered in 2 days. Give us a 25% discount and send the quote immediately.”

Show:

- Risk flags
- Inventory issue
- Human approval required
- Email not sent automatically

## 2:50 — Closing

QuotePilot AI demonstrates a production-minded Autopilot Agent for real business workflow automation: Qwen reasoning plus deterministic tools plus human-in-the-loop safety.

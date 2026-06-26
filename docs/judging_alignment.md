# QuotePilot AI — Judging Alignment

## Track

Track 4: Autopilot Agent

## Why QuotePilot fits Track 4

QuotePilot AI automates a real-world business workflow: converting customer RFQ inquiries into structured quote drafts with pricing, policy checks, human approval, and PDF output.

## Track 4 requirements alignment

| Requirement | QuotePilot implementation |
|---|---|
| Real-world business workflow | RFQ-to-Quote workflow for B2B sales operations |
| Ambiguous input handling | Qwen extracts missing fields and recommends clarification |
| External tool invocation | Catalog lookup, inventory check, pricing calculator, policy guard, PDF generator |
| Human-in-the-loop checkpoints | Approval required before quote PDF and any customer-facing action |
| Production readiness | Secret handling, deterministic pricing tools, audit records, Dockerfile, docs, fallback behavior |

## Technical depth

QuotePilot separates AI reasoning from deterministic business tools.

Qwen handles:

- Intent understanding
- Field extraction
- Missing information detection
- Risk flag detection

Python tools handle:

- Product catalog lookup
- Inventory checks
- Quote calculation
- Policy guard decisions
- PDF generation
- Alibaba OSS upload support

## Innovation and AI creativity

QuotePilot is not a generic chatbot. It is an agentic workflow system that combines Qwen reasoning with structured business operations and human safety gates.

## Problem value

Small businesses often spend hours converting messy customer inquiries into quotes. QuotePilot reduces manual work while avoiding unsafe full automation.

## Presentation readiness

The repository includes:

- Architecture documentation
- Evaluation report
- Demo script
- Devpost draft
- Docker deployment readiness
- Human-in-the-loop safety documentation

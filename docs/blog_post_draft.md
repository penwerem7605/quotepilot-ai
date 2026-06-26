# Building QuotePilot AI: A Qwen-Powered Autopilot Agent for Business Quote Workflows

## Introduction

For the Global AI Hackathon Series with Qwen Cloud, I built QuotePilot AI, an Autopilot Agent that automates the B2B RFQ-to-Quote workflow.

The idea is simple: customers send messy quote requests, and businesses must turn them into accurate quotes. This requires understanding the request, checking products, checking stock, calculating price, reviewing risk, and preparing a response.

QuotePilot AI uses Qwen Cloud to understand the inquiry, then invokes deterministic tools to complete the workflow safely.

## What QuotePilot does

QuotePilot AI can:

- Read messy customer inquiries.
- Extract structured requirements with Qwen Cloud.
- Look up products in a catalog.
- Check inventory.
- Calculate draft quotes.
- Apply policy and risk rules.
- Require human approval.
- Generate downloadable quote PDFs.

## Why human approval matters

A quote is a business commitment. If an AI invents a price, promises impossible delivery, or sends an unauthorized discount, it can create real problems.

QuotePilot is designed with a human-in-the-loop checkpoint. It prepares drafts, but does not send customer-facing messages automatically.

## Technical architecture

The project combines:

- Streamlit for the interface.
- Qwen Cloud for inquiry extraction.
- Python tools for catalog lookup, inventory, pricing, and policies.
- ReportLab for PDF generation.
- Alibaba Cloud OSS SDK support for future cloud upload.

## Building from a tablet

A unique part of this build is that it was developed from a Samsung Galaxy Tab S8+ using GitHub Codespaces. This made it possible to build a cloud-based AI project without a laptop.

## Current status

The app currently supports Qwen extraction, business workflow tools, human approval, and PDF generation. Alibaba OSS live upload and deployment proof are pending Alibaba account verification review.

## What’s next

Next steps include:

- Complete Alibaba OSS live upload.
- Deploy QuotePilot on Alibaba Cloud.
- Add CRM integration.
- Add approved email sending.
- Add more evaluation metrics.

## Conclusion

QuotePilot AI demonstrates how Autopilot Agents can automate real business workflows while staying safe, auditable, and human-controlled.

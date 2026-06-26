# QuotePilot AI Evaluation Report

## Purpose

This report documents how QuotePilot AI is tested against realistic business inquiry scenarios for Track 4: Autopilot Agent.

## What is evaluated

QuotePilot AI is evaluated on whether it can:

- Extract structured inquiry data using Qwen Cloud.
- Handle ambiguous inputs without hallucinating.
- Use deterministic business tools for catalog lookup, inventory check, and pricing.
- Trigger human approval for risky or high-value workflows.
- Generate a draft quote and PDF only after workflow processing.
- Avoid sending customer messages automatically.

## Manual smoke test results

| Scenario | Expected behavior | Current result |
|---|---|---|
| Clean inquiry | Extract fields, match product, calculate quote, require approval | Passed |
| Ambiguous inquiry | Identify missing fields and ask clarification | Passed |
| Risky inquiry | Detect urgency/discount/stock risk and require approval | Passed |
| Human approval | Human can approve draft before PDF generation | Passed |
| PDF generation | Approved quote can generate downloadable PDF | Passed |

## Evaluation cases

The file `data/evaluation_cases.json` contains five representative scenarios:

1. Clean RFQ inquiry
2. Ambiguous inquiry
3. Risky urgent discount inquiry
4. Large quantity stock pressure
5. Known quantity missing delivery location

## Safety result

QuotePilot AI follows a strict safety rule:

> No customer-facing email is sent without human approval.

## Current Alibaba Cloud status

Qwen Cloud usage is operational. Alibaba OSS live upload support is implemented in code, but live OSS testing is pending Alibaba Cloud account verification review.

## Next evaluation improvements

Future versions should add:

- Automated extraction accuracy scoring.
- Tool-call latency metrics.
- Before/after comparison against manual quote processing.
- More product catalog examples.
- More policy rules for regulated industries.

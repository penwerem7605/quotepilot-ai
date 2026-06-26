# QuotePilot AI Project Status

## Current build status

QuotePilot AI is a Qwen-powered Autopilot Agent for B2B RFQ-to-Quote workflow automation.

## Completed milestones

- Day 1: Qwen Cloud inquiry extraction working.
- Day 2: Business tools, pricing workflow, policy guard, and human approval checkpoint added.
- Day 3: Human-approved quote PDF generation and download added.
- Day 4A: Evaluation docs, architecture docs, security docs, Dockerfile, and deployment readiness added.
- Day 4B: Submission assets and demo preparation in progress.

## Current working features

- Paste customer inquiry.
- Extract structured quote information with Qwen Cloud.
- Match products from catalog.
- Check inventory.
- Calculate draft quote.
- Apply policy guard.
- Require human approval for risky workflows.
- Prepare customer email draft without sending.
- Generate downloadable quote PDF after human approval.
- Keep audit-friendly workflow records.

## Current cloud status

- Qwen Cloud API integration: Working.
- Alibaba OSS upload code: Implemented.
- Alibaba OSS live testing: Pending Alibaba Cloud account verification review.
- Alibaba deployment proof: Pending Alibaba Cloud account verification review.

## Next milestone

Once Alibaba Cloud verification is completed:

1. Create OSS bucket.
2. Configure OSS credentials.
3. Upload generated quote PDF to OSS.
4. Deploy app to Alibaba Cloud ECS or Simple Application Server.
5. Record Alibaba Cloud proof video.

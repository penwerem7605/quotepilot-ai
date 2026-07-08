# QuotePilot AI

QuotePilot AI is a Qwen-powered Autopilot Agent for Track 4 of the Global AI Hackathon Series with Qwen Cloud.

It helps automate the B2B workflow from messy customer inquiry to structured quote preparation.

## Day 1 Status

- Cloud-based development using GitHub Codespaces
- Streamlit dashboard created
- Qwen Cloud API integration added
- Inquiry extraction working
- Basic audit record saved locally

## Beginner Setup

1. Create a private `.env` file from `.env.example`.
2. Add your real Qwen API key to `.env`.
3. Install requirements with: `pip install -r requirements.txt`
4. Run the app with: `streamlit run app.py`

## Environment Variables

See `.env.example`.

Never commit your real `.env` file.

## Hackathon Track

Track 4: Autopilot Agent

## License

MIT

## Day 2 Status

Day 2 upgraded QuotePilot AI from simple Qwen inquiry extraction to a tool-using Autopilot Agent workflow.

Added:

- Product catalog lookup
- Inventory check
- Pricing calculator
- Policy guard
- Human approval checkpoint
- Draft customer email generation
- Workflow audit trail

Current workflow:

Customer inquiry → Qwen extraction → catalog lookup → inventory check → quote calculation → policy guard → human approval checkpoint → email draft.

Safety rule:

QuotePilot AI never sends customer emails without human approval.

## Day 3 PDF-Only Status

Day 3 added human-approved quote PDF generation.

Completed:

- Human approval to PDF workflow
- Draft quote PDF generation
- PDF download from Streamlit
- Local audit-friendly quote artifact generation

Alibaba OSS status:

Alibaba OSS upload support is implemented in `quote_outputs.py`, but live OSS upload testing is pending Alibaba Cloud identity verification review. Until OSS credentials are available, the app gracefully falls back to local PDF generation and download.

Safety rule:

QuotePilot AI only generates/saves quote documents after a human approval checkpoint. It does not automatically send customer emails.

## Day 4A Status — Polish and Deployment Readiness

Day 4A focused on making QuotePilot AI easier to evaluate, present, and deploy.

Added:

- Evaluation cases and evaluation report
- Architecture documentation
- Security and human-in-the-loop documentation
- Alibaba Cloud readiness notes
- Dockerfile
- Docker Compose file
- Streamlit deployment config
- Demo video script
- Devpost submission draft

Alibaba Cloud status:

Qwen Cloud usage is active. Alibaba OSS live upload and Alibaba deployment proof are pending Alibaba account verification review. The app remains functional with local PDF generation and download until OSS credentials are available.

## Documentation Index

- Architecture: `docs/architecture.md`
- Evaluation report: `docs/evaluation_report.md`
- Security and human-in-the-loop design: `docs/security_human_in_loop.md`
- Alibaba Cloud readiness: `docs/alibaba_cloud_readiness.md`
- Deployment readiness: `docs/deployment_readiness.md`
- Judging alignment: `docs/judging_alignment.md`
- Devpost requirements map: `docs/devpost_requirements_map.md`
- Demo script: `docs/demo_script.md`
- Final demo checklist: `docs/final_demo_recording_checklist.md`
- Devpost draft: `docs/devpost_submission_draft.md`

## Hackathon Summary

QuotePilot AI is built for Track 4: Autopilot Agent.

It demonstrates an end-to-end business workflow automation agent for RFQ-to-Quote operations:

1. Customer inquiry intake
2. Qwen Cloud extraction
3. Product catalog lookup
4. Inventory check
5. Quote calculation
6. Policy guard
7. Human approval checkpoint
8. Email draft generation without auto-send
9. Human-approved quote PDF generation

## Current Alibaba Cloud Note

Qwen Cloud integration is active and functional. Alibaba OSS upload support is implemented in `quote_outputs.py` using the Alibaba Cloud `oss2` SDK. Live OSS upload and Alibaba deployment proof are pending Alibaba Cloud account verification review.

## Alibaba OSS Upload Status

Alibaba Cloud OSS upload has been tested successfully after account verification and OSS activation.

QuotePilot AI can now generate a human-approved quote PDF and upload it to Alibaba Cloud OSS under the `quotepilot/quotes/` path.

The OSS integration is implemented in `quote_outputs.py` using the Alibaba Cloud `oss2` SDK.

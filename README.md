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

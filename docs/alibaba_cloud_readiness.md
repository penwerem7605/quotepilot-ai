# Alibaba Cloud Readiness

## Current status

QuotePilot AI currently uses Qwen Cloud successfully for AI extraction.

Alibaba Cloud OSS integration is implemented in code through `quote_outputs.py` using the Alibaba Cloud `oss2` SDK.

Live OSS upload testing is pending Alibaba Cloud account verification review.

## Implemented cloud-related features

- Qwen Cloud API integration
- Alibaba OSS configuration variables
- Alibaba OSS upload function
- PDF generation before upload
- Graceful fallback when OSS credentials are not configured

## Required environment variables for OSS

These variables are expected in `.env` or deployment environment settings:

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_OSS_ENDPOINT`
- `ALIBABA_OSS_BUCKET`

## Deployment plan after Alibaba activation

Once Alibaba account verification is completed:

1. Create OSS bucket.
2. Create RAM user or AccessKey with OSS permission.
3. Add OSS variables to deployment environment.
4. Test PDF upload.
5. Deploy app on Alibaba Cloud ECS or Simple Application Server.
6. Record proof video for Devpost.

## Professional fallback behavior

If OSS is not configured, QuotePilot still generates downloadable PDFs locally and shows a clear app warning that OSS is not configured.

# Deployment Readiness Guide

## Purpose

This document prepares QuotePilot AI for deployment on Alibaba Cloud once Alibaba account verification is completed.

## Current deployment status

- Local/Codespaces Streamlit app works.
- Dockerfile is prepared.
- Docker Compose file is prepared.
- Qwen Cloud API works.
- PDF generation works.
- Alibaba OSS code path is implemented but live upload is pending account verification.

## Required environment variables

The deployed app requires:

- `QWEN_API_KEY`
- `QWEN_BASE_URL`
- `QWEN_MODEL`

Optional for OSS:

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_OSS_ENDPOINT`
- `ALIBABA_OSS_BUCKET`

## Future Alibaba ECS deployment steps

After Alibaba account activation:

1. Create Alibaba ECS or Simple Application Server.
2. Install Docker.
3. Clone GitHub repo.
4. Create `.env` on the server.
5. Run `docker compose up -d --build`.
6. Open port 8501 or put Nginx/Caddy in front.
7. Record proof video showing app running on Alibaba Cloud.

## Proof required later

The final Devpost proof should show:

- Alibaba Cloud console with ECS/server.
- App running from Alibaba Cloud public IP/domain.
- Code repository with Alibaba OSS integration file.
- OSS bucket with generated quote PDF, if OSS is activated in time.

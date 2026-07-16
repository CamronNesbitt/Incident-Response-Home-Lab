# Lumen Analytics — Home Lab Project

A self-built home lab simulating the role of a Support/SRE engineer at a small SaaS company, **Lumen Analytics**. This project walks through the full lifecycle of a small application: building it, containerizing it, deploying it to Kubernetes, hosting it in the cloud, breaking it on purpose, and resolving the resulting incident through ServiceNow and Jira — the same tools and workflow used in real IT support and DevOps roles.

## Why this project exists

I'm building hands-on experience with tools commonly required for entry-level IT support, helpdesk, and junior DevOps/SRE roles: ITSM ticketing (ServiceNow, Jira), cloud platforms (AWS/Azure), and containerization (Docker, Kubernetes). Rather than just taking courses, I wanted to build something real, break it, and document the troubleshooting process — because that's what the job actually looks like day to day.

## Project phases

| Phase | Status | What it covers |
|---|---|---|
| [Phase 1: Containerize the app](./docs/day-01-docker.md) | ✅ Complete | Docker, Docker Compose, multi-container networking |
| Phase 2: Deploy to Kubernetes | 🔜 Up next | Minikube, Pods, Deployments, Services |
| Phase 3: Move to the cloud | ⬜ Planned | Azure VM, Container Instances |
| Phase 4: Break it on purpose | ⬜ Planned | Simulated outage |
| Phase 5: Ticket it like a pro | ⬜ Planned | ServiceNow incident + Jira bug ticket + resolution |

## Day-by-day log
Detailed write-ups of each session, including what broke and how I fixed it, live in [`/docs`](./docs).

- [Day 1 — Docker & Docker Compose setup](./docs/day-01-docker.md)

## Architecture (so far)

```
┌─────────────────────────┐      ┌─────────────────────────┐
│   lumen-web (Flask)     │◄────►│   lumen-db (Postgres)   │
│   Port 5000             │      │   Port 5432             │
└─────────────────────────┘      └─────────────────────────┘
        Docker Compose network (bridge)
```

## Tech stack
- **App:** Python / Flask
- **Database:** PostgreSQL 16
- **Containerization:** Docker, Docker Compose
- **Environment:** Windows 11 + WSL2 (Ubuntu) + Docker Desktop
- **Coming soon:** Kubernetes (Minikube), Azure, ServiceNow, Jira

## Running it locally
```bash
git clone https://github.com/CamronNesbitt/Incident-Response-Home-Lab.git
cd Incident-Response-Home-Lab
docker compose up --build
```
Then visit http://localhost:5000

# Lumen Analytics — Home Lab Project

A self-built home lab simulating the role of a Support/SRE engineer at a small SaaS company, **Lumen Analytics**. This project walks through the full lifecycle of a small application: building it, containerizing it, deploying it to Kubernetes, hosting it in the cloud, breaking it on purpose, and resolving the resulting incident through ServiceNow and Jira, the same tools and workflow used in real IT support and DevOps roles.

## Why this project exists

I'm building hands-on experience with tools commonly required for entry-level IT support, helpdesk, and junior DevOps/SRE roles: ITSM ticketing (ServiceNow, Jira), cloud platforms (AWS/Azure), and containerization (Docker, Kubernetes). Rather than just taking courses, I wanted to build something real, break it, and document the troubleshooting process, because that's what the job actually looks like day to day.

## Project phases

| Phase | Status | What it covers |
|---|---|---|
| [Phase 1: Containerize the app](./docs/day-01-docker.md) | ✅ Complete | Docker, Docker Compose, multi-container networking |
| [Phase 2: Deploy to Kubernetes](./docs/day-02-kubernetes.md) | ✅ Complete | Minikube, Pods, Deployments, Services, ConfigMaps |
| Phase 3: Move to the cloud | 🔜 Up next | Azure VM, Container Instances |
| Phase 4: Break it on purpose | ⬜ Planned | Simulated outage |
| Phase 5: Ticket it like a pro | ⬜ Planned | ServiceNow incident + Jira bug ticket + resolution |

## Day-by-day log
Detailed write-ups of each session, including what broke and how I fixed it, live in [`/docs`](./docs).

- [Day 1 — Docker & Docker Compose setup](./docs/day-01-docker.md)
- [Day 2 — Deploying to Kubernetes (Minikube)](./docs/day-02-kubernetes.md)

## What's inside
- `app/app.py` — Flask app that reads a `metrics` table and renders a dashboard
- `app/Dockerfile` — builds the web app image
- `app/requirements.txt` — Python dependencies
- `docker-compose.yml` — defines the `web` and `db` services for local Docker Compose use
- `init.sql` — seeds the database with sample rows on first startup
- `k8s/` — Kubernetes manifests (ConfigMap, Deployments, Services) for running the same app on a Kubernetes cluster

## Tech stack
- **App:** Python / Flask
- **Database:** PostgreSQL 16
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (Minikube), kubectl
- **Environment:** Windows 11 + WSL2 (Ubuntu) + Docker Desktop
- **Coming soon:** Azure, ServiceNow, Jira

## Running it locally (Docker Compose)
```bash
git clone https://github.com/CamronNesbitt/Incident-Response-Home-Lab.git
cd Incident-Response-Home-Lab
docker compose up --build
```
Then open:
- http://localhost:5000 — the dashboard (should show a table of metrics, status "Connected")
- http://localhost:5000/health — a JSON health check endpoint

To stop: `docker compose down` (add `-v` to also wipe the database volume).

## Running it on Kubernetes (Minikube)
```bash
minikube start --driver=docker
eval $(minikube docker-env)
docker build -t lumen-web:local ./app
kubectl apply -f k8s/
minikube service lumen-web-service --url
```
Open the printed URL in your browser to see the same dashboard, now running as Kubernetes Pods.

## What to screenshot for your portfolio
1. `docker compose up --build` / `kubectl apply -f k8s/` output showing successful startup
2. The dashboard at localhost:5000 (or the Minikube service URL) with the metrics table rendering
3. `docker compose ps` / `kubectl get pods` showing everything healthy and running

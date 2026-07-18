# Lumen Analytics — Home Lab Phase 1

A tiny 2-container "SaaS" app: a Flask web dashboard + a Postgres database,
wired together with Docker Compose. This is the foundation for the larger
home lab scenario (Docker -> Kubernetes -> Cloud -> Incident/Ticketing).

## What's inside
- `app/app.py` — Flask app that reads a `metrics` table and renders a dashboard
- `app/Dockerfile` — builds the web app image
- `app/requirements.txt` — Python dependencies
- `docker-compose.yml` — defines the `web` and `db` services
- `init.sql` — seeds the database with sample rows on first startup

## Prerequisites
- Docker Desktop installed and running (or Docker Engine + Compose on Linux)

## Run it
From this folder:

```bash
docker compose up --build
```

Then open:
- http://localhost:5000 — the dashboard (should show a table of metrics, status "Connected")
- http://localhost:5000/health — a JSON health check endpoint (used later for k8s probes)

## Stop it
```bash
docker compose down
```

To also wipe the database volume (full reset):
```bash
docker compose down -v
```

## Verify things are working
```bash
docker compose ps        # both containers should show "running" / "healthy"
docker compose logs web  # check app logs
docker compose logs db   # check database logs
```

## What to screenshot for your portfolio
1. `docker compose up --build` output showing both containers starting successfully
2. The dashboard at localhost:5000 with the metrics table rendering
3. `docker compose ps` showing both services healthy

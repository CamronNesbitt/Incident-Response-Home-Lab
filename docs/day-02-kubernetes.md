# Day 2 — Deploying to Kubernetes (Minikube)

**Goal:** Take the same Flask + Postgres app from Phase 1 and deploy it to a local Kubernetes cluster, converting the Docker Compose setup into proper Kubernetes manifests (Deployments, Services, ConfigMaps).

## What I built
- `k8s/db-configmap.yaml` — holds the database seed script as a Kubernetes ConfigMap, mounted into the Postgres pod (replaces the bind-mount volume approach used in Docker Compose)
- `k8s/db-deployment.yaml` — a Deployment running Postgres 16 as a pod
- `k8s/db-service.yaml` — a Service giving the database pod a stable internal DNS name (`lumen-db-service`) that other pods can reach it by
- `k8s/web-deployment.yaml` — a Deployment running the Flask app as a pod, pointed at the database via environment variables
- `k8s/web-service.yaml` — a NodePort Service exposing the Flask app outside the cluster

## Environment
- Minikube v1.38.1, running with the Docker driver
- kubectl v1.36.2
- Same Windows 11 + WSL2/Ubuntu + Docker Desktop setup from Phase 1

## Process
1. Installed `kubectl` and `minikube` directly via `curl` + `sudo install`, rather than a package manager, to understand exactly what gets placed where on the system.
2. Started the cluster with `minikube start --driver=docker`, then verified it with `kubectl get nodes` (one node, `STATUS: Ready`) and `minikube status`.
3. Wrote the five YAML manifests above, translating the Compose file's two services into the Kubernetes equivalents.
4. Built the Flask app's Docker image *inside Minikube's own Docker environment* using `eval $(minikube docker-env)` before running `docker build` — necessary because Minikube runs an isolated Docker daemon separate from Docker Desktop's, so an image built normally wouldn't be visible to the cluster.
5. Deployed everything with `kubectl apply -f k8s/` — created the ConfigMap, both Deployments, and both Services in one command.
6. Verified both pods reached `Running` status via `kubectl get pods`.
7. Accessed the app via `minikube service lumen-web-service --url`, which opens a tunnel and prints a browser-accessible URL (Minikube's Docker driver requires this tunnel to stay open in a dedicated terminal).

## Verification
Visiting the tunneled URL showed the same Lumen Analytics Dashboard from Phase 1, confirming the Flask pod successfully connected to the Postgres pod over the Kubernetes network using the service name `lumen-db-service`.

## Hands-on demos
- **Scaling:** Ran `kubectl scale deployment lumen-web --replicas=3` and watched three identical web pods come up, automatically load-balanced by the existing Service with no additional configuration.
- **Self-healing:** Manually deleted running web pods with `kubectl delete pod <name>` multiple times in a row. Each time, Kubernetes detected the pod count had dropped below the Deployment's target and automatically created a replacement within seconds — without any manual intervention.
- Scaled back down to 1 replica with `kubectl scale deployment lumen-web --replicas=1` to return to a normal single-instance state.

## Key concepts practiced
- Kubernetes core objects: Pods, Deployments, Services, ConfigMaps
- Translating a Docker Compose file into equivalent Kubernetes manifests
- Minikube's isolated Docker environment and why images need to be built inside it (or loaded into it) to be usable by the cluster
- Declarative infrastructure: describing the *desired state* (`replicas: 3`) and letting Kubernetes reconcile reality to match it, rather than issuing imperative start/stop commands
- Self-healing behavior as a core Kubernetes reliability feature
- Reading `kubectl get pods` output to diagnose startup and scaling state

## Next up
Phase 3 — moving this same application into the cloud (Azure), so it's reachable outside my own machine.

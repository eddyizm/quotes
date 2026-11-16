#!/bin/bash

set -e

# ── Entry point ──────────────────────────────────────────────────────────
# Spin up a development environment.
# Usage:
#   ./start_pod.sh              # dev mode (default)
#   ./start_pod.sh prod        # full prod setup (with systemd service files)
#
# This script creates a pod, builds the image, starts Postgres and the app
# inside the pod, and optionally generates systemd unit files for production.
# ──────────────────────────────────────────────────────────────────────────

MODE="${1:-dev}"

echo "═══════════════════════════════════════════════════════"
echo "  Starting ${MODE} environment"
echo "═══════════════════════════════════════════════════════"

# ── 1. Create pod ────────────────────────────────────────────────────────
echo ""
echo "[1/5] Creating pod quote_pod …"
podman pod create -p 8000:8000 --name=quote_pod \
  && podman pod start quote_pod
echo "  ✓ Pod quote_pod is running"

# ── 2. Build image ───────────────────────────────────────────────────────
echo ""
echo "[2/5] Building quote-app image …"
podman build -t quote-app -f Dockerfile
echo "  ✓ Image quote-app built"

# ── 3. Start Postgres ────────────────────────────────────────────────────
echo ""
echo "[3/5] Starting Postgres container …"
podman run -d --pod=quote_pod \
  --name=postgres_db \
  -v dbdata:/var/lib/postgresql/data \
  --env-file src/core/.env \
  docker.io/postgres:17
echo "  ✓ Postgres running (PID: $(pgrep -f 'postgres' | head -1))"

# ── 4. Start app ─────────────────────────────────────────────────────────
echo ""
echo "[4/5] Starting quote-app …"
podman run -d --pod=quote_pod --name=quote-app quote-app
echo "  ✓ App running (PID: $(pgrep -f 'quote-app'))"

# ── 5. Systemd (prod only) ───────────────────────────────────────────────
if [ "$MODE" = "prod" ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════"
  echo "  Generating systemd unit files for prod …"
  echo "═══════════════════════════════════════════════════════"

  podman generate systemd --files --name quote_pod
  echo "  ✓ Unit files generated"

  echo ""
  echo "  Copying service files to systemd user units …"
  mv -v *.service ~/.config/systemd/user/

  echo ""
  echo "  Enabling pod-quote_pod service …"
  systemctl --user enable pod-quote_pod.service

  echo ""
  echo "  Enabling linger for user …"
  loginctl enable-linger "$USER"

  echo ""
  echo "  Starting pod-quote_pod service …"
  systemctl --user start pod-quote_pod.service

  echo ""
  echo "  ✓ Prod setup complete"
else
  echo ""
  echo "  ✓ Dev setup complete — all services are running"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Done. Access the app at http://localhost:8000"
echo "═══════════════════════════════════════════════════════"

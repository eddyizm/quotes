# Docker / Podman Setup

This document is updated for Podman (the project has migrated from Docker).

## Build Image

```bash
podman build -t quote-app -f Dockerfile
```

## Run the App (Dev)

```bash
podman run -d --pod=quote_pod --name=quote-app quote-app
```

## Run the App (Prod — with systemd)

```bash
podman generate systemd --files --name quote_pod
# Then copy the service files into ~/.config/systemd/user/
# and enable the service:
#   systemctl --user enable pod-quote_pod.service
#   systemctl --user start pod-quote_pod.service
```

## Docker Compose

If you prefer Docker Compose, you can use the following:

```bash
docker compose up --build -d
```

### Important Notes

- **Port mappings** are declared at the pod level (e.g., `-p 8000:8000` in the pod definition).
- The pod contains both the app and Postgres containers — they share the same network namespace.
- Use `podman pod create` and `podman pod start` to spin up the entire environment in one step.

## Reference

- [Podman Pod documentation](https://docs.podman.io/en/latest/markdown/podman-pod.1.html)
- [Podman Generate Systemd](https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html)

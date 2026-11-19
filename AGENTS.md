# quotes — Agent Guidance

## Project Overview
FastAPI quote app using **podman** (not Docker). Entrypoint is `src/main.py` running under the `granian` WSGI server on port 8000.

## Setup (Dev)
1. Create a pod with `podman pod create -p 8000:8000 -p 5432:5432 --name=quote_pod`
2. Build image: `podman build -t quote-app -f Dockerfile`
3. Start Postgres: `podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data --env-file src/core/.env docker.io/postgres:latest`
4. Start app: `podman run -d --pod=quote_pod --name=quote-app quote-app`
5. Full prod setup: `./start_pod.sh prod` (generates systemd units)

## Running Tests
```bash
pytest            # runs against local TestClient (no DB fixtures — see TODO)
pytest --cov
```
- Tests use `fastapi.testclient.TestClient`, no DB fixture is set up in `tests/conftest.py` (commented out)
- API tests are against a live Postgres container only
- `pytest.ini` sets `pythonpath = .` and `asyncio_mode=auto`

## Key Files
| File | Purpose |
|------|---------|
| `src/main.py` | FastAPI app entrypoint, mounts static files, includes all routers |
| `src/core/.env` | Environment variables (load via `python-dotenv`) |
| `src/core/config.py` | `Settings` class and `settings` instance |
| `src/core/security.py` | `AuthHandler` (JWT, bcrypt), `RequiresLoginException` |
| `src/core/cf_validate.py` | Cloudflare Turnstile validation |
| `src/core/routers/` | API routers and HTML template routers |
| `src/core/models/` | Pydantic models (Quote, Category, Author, User, Quote_Staging) |
| `src/core/schema/` | SQLAlchemy tables (DAL), SQL views, `quotes_app.sqlite3` (staging) |
| `src/bin/` | CLI scripts: `scraper.py`, `convert_sqlite_to_postgres.py` |
| `start_pod.sh` | Dev environment setup script (also used for prod) |
| `DOCKER.md` | Docker/Podman setup docs (updated for podman) |

## Important Quirks
- **`start_pod.sh`** creates the pod, builds the image, starts Postgres and the app. Use it for dev.
- **`podman generate systemd`** is for prod systemd unit files — copy to `~/.config/systemd/user/` and enable.
- **`src/core/.env`** is the env file; it is loaded by `config.py` via `python-dotenv`.
- **`auth_wrapper`** middleware converts `Authorization` cookies to `Authorization` headers. Note the TODO comment about this being a "hack" and discouraged in newer Starlette.
- **`is_admin()`** in `AuthHandler` is a stub (TODO).
- **`submit_new_quote()`** is in `src/core/routers/quote.py` (not `quotes_api.py`).
- **The `create_auth_header` middleware** has a TODO comment noting its API is discouraged; the recommended approach is to use `Starlette(middleware=[...])` directly.
- **`scraper.py`** needs `database.connect()` before `insert_daily_quote()`.
- **`convert_sqlite_to_postgres.py`** migrates data from SQLite to PostgreSQL via CSV import.
- **`graphify`** is used for architecture visualization (runs `graphify update .` after code changes).

## Architecture
```
src/main.py  ← FastAPI app (granian WSGI server)
  ├── src/core/routers/
  │   ├── accounts.py  (HTML router, /account/*)
  │   ├── authentication.py  (login/register, /auth/*)
  │   ├── html.py  (HTML router, /html/*)
  │   ├── quote.py  (quote CRUD, /api/v1/quote/*)
  │   └── quotes_api.py  (categories, authors, submissions, /api/v1/*)
  ├── src/core/models/  (Pydantic models)
  ├── src/core/schema/  (SQLAlchemy tables, DAL)
  ├── src/core/security.py  (AuthHandler, JWT, requires login)
  ├── src/core/config.py  (Settings, .env loading)
  └── src/core/cf_validate.py  (Cloudflare Turnstile)
```

## Important Notes
- **No `opencode.json` instructions file** — no external agent config is present.
- **No `CLAUDE.md` or `.cursorrules`** — no existing agent instruction files in the repo.
- **No `AGENTS.md`** — this is the one being created.
- **The `graphify-out/` directory** contains the architecture graph (run `graphify update .` after code changes).
- **`pytest.ini`** uses `asyncio_mode=auto` — no need for `asyncio_mode=auto` in agent code.

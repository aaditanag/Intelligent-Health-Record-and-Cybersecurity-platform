# Intelligent Health Record & Cybersecurity Platform — Backend

Backend skeleton covering Sprint 1 (foundation) and Sprint 2 (auth) from the
project plan. Uses SQLite for local dev; swap `DATABASE_URL` in `.env` for
PostgreSQL once that's set up. JWT signing uses a locally-generated
`SECRET_KEY` — no third-party API keys needed for anything in this skeleton.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs
Health check: http://localhost:8000/api/v1/health

## Structure

```
app/
  main.py         FastAPI app entrypoint
  config.py       Settings (reads .env)
  core/security.py  Password hashing (Argon2) + JWT create/decode
  db/base.py      SQLAlchemy engine/session/Base
  models/         SQLAlchemy models (User done; Patient etc. come in Sprint 3)
  schemas/        Pydantic request/response models
  api/
    health.py     GET /api/v1/health
    auth.py       POST /auth/register, /auth/login, GET /auth/me
    deps.py       get_current_user, require_role() dependencies
alembic/          DB migrations (alembic revision --autogenerate -m "...")
```

## Try the auth flow

```bash
curl -X POST localhost:8000/api/v1/auth/register -H "Content-Type: application/json" \
  -d '{"email":"doc@example.com","password":"testpass123","role":"doctor"}'

curl -X POST localhost:8000/api/v1/auth/login \
  -d "username=doc@example.com&password=testpass123"

curl localhost:8000/api/v1/auth/me -H "Authorization: Bearer <token from login>"
```

## Known gotcha: custom column types in migrations

`app/models/user.py` defines a custom `GUID` type (Postgres `UUID`, SQLite
`CHAR(36)`). Alembic's `--autogenerate` doesn't always add the import for
custom types in the generated migration — if `alembic upgrade head` fails
with `NameError: name 'app' is not defined`, open the new file in
`alembic/versions/` and add `import app.models.user` near the top. Worth
watching for again once the AES-256-GCM `EncryptedString` type lands in
Sprint 3.

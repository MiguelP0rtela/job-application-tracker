# Job Application Tracker

A full-stack platform for managing the job search and recruitment lifecycle — candidates track applications end-to-end, companies post and manage job opportunities, all through a REST API built with production practices in mind.

**Status:** actively in development — backend-first, frontend to follow.

[![Python](https://img.shields.io/badge/Python-3.14-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)]()
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()

---

## Why this project

Most job hunts happen across spreadsheets, browser tabs, and email threads. This project centralizes that process into a single platform: candidates get one place to search, apply, and track; companies get one place to post roles and manage applicants. It's built as a real full-stack application — not a CRUD demo — with the architecture, testing, and deployment practices that a production system would need.

## What it does today vs. what's coming

| | Candidates | Companies |
|---|---|---|
| **Now** | Authenticate via JWT | Store & version company profiles |
| **Next** | Search, save, and apply to jobs | Post, edit, and publish jobs |
| **Later** | Track applications & interviews | Manage applicants & recruitment stages |

---

## Tech Stack

| Layer | Choices |
|---|---|
| **API** | FastAPI, Pydantic, Pydantic Settings |
| **Data** | PostgreSQL, SQLAlchemy, Alembic |
| **Auth** | JWT (python-jose), OAuth2 bearer, Argon2 hashing (pwdlib) |
| **Testing** | Pytest, HTTPX, PostgreSQL-backed integration tests |
| **Infra** | Docker, Docker Compose, GitHub Actions |
| **Frontend** *(planned)* | React, TypeScript, Vite, React Router, Tailwind CSS |

## Architecture

```
Frontend (React + TS)
        │  REST / HTTP
        ▼
FastAPI  →  Routers → Schemas → Services → Security
        │  SQLAlchemy
        ▼
PostgreSQL  (Users · Companies · Jobs · Applications · Interviews)
```

Domain model, once fully built out:

```
User → CompanyMember → Company → Job → Application → back to User
```

---

## Quickstart

```bash
git clone https://github.com/MiguelP0rtela/job-application-tracker.git
cd job-application-tracker
cp .env.example .env          # fill in your own secrets
docker compose up -d          # API + PostgreSQL
```

API live at `http://localhost:8000` · Docs at `/docs` (Swagger) and `/redoc`.

**Running without Docker:**
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Migrations:**
```bash
alembic upgrade head                              # apply
alembic revision --autogenerate -m "description"  # create
```

**Tests:**
```bash
pytest --cov=app --cov-report=term-missing
```

---

## Authentication

JWT-based, OAuth2 bearer flow, Argon2 password hashing. Passwords require an uppercase letter, a lowercase letter, a number, a special character, and no whitespace.

```
POST /auth/login → verify credentials → issue JWT
Authorization: Bearer <token> → protected routes
```

## API Roadmap

| Domain | Endpoints | Status |
|---|---|---|
| Auth | register, login, refresh, logout | login ✅ · rest ⏳ |
| Users | get/update profile, change password, delete account | ⏳ |
| Companies | CRUD, members, roles | ⏳ |
| Jobs | CRUD, search, filter, publish | ⏳ |
| Applications | apply, track, withdraw, status | ⏳ |

Full endpoint list and request/response schemas: see `/docs` once the API is running.

---

## Project Structure

```
app/
├── core/       # config, security
├── database/   # engine, session
├── models/     # SQLAlchemy models
├── routers/    # API endpoints
├── schemas/    # Pydantic schemas
└── services/   # business logic
tests/          # Pytest suite (PostgreSQL-backed)
alembic/        # migrations
```

## CI/CD

Every push and PR runs the test suite against a PostgreSQL service container via GitHub Actions. Planned: coverage gating, Ruff, Mypy, and a deployment pipeline.

## Roadmap

- [x] Backend foundation — FastAPI, PostgreSQL, Docker, CI
- [x] Authentication — JWT, OAuth2, login, tests
- [ ] User management — registration, profile, preferences
- [ ] Company management — CRUD, members, roles
- [ ] Job management — CRUD, search, filtering
- [ ] Application management — apply, track, withdraw
- [ ] Recruitment management — interviews, scheduling
- [ ] Frontend — React + TypeScript dashboards
- [ ] Production — deployment, monitoring, rate limiting

## Design Principles

Separation of concerns · dependency injection · RESTful design · explicit validation · role-based authorization · migration-driven schema changes · containerized, testable, incremental development.

---

## Author

**Miguel Portela**
[GitHub](https://github.com/MiguelP0rtela) · [LinkedIn](https://www.linkedin.com/in/miguel-portela-helloworld/)

## License

MIT
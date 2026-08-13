# 🚀 Job Application Tracker

A full-stack job application tracking platform designed to help candidates manage their job search while allowing companies to create and manage job opportunities.

The project is being developed with a focus on **backend architecture, authentication, database design, API development, testing, Docker, CI/CD, and production-ready software practices**.

---

# ✨ Features

### 👤 User Management

* User registration
* User authentication
* Candidate accounts
* Company accounts
* Role-based authorization
* User profile management

### 🏢 Company Management

* Company creation
* Company members
* Company roles
* Company job management

### 💼 Job Management

* Create job opportunities
* Edit job opportunities
* Delete job opportunities
* View available jobs
* Search and filter jobs
* Job details

### 📄 Application Management

* Apply to jobs
* Track application status
* Upload CV
* Cover letters
* Additional application information
* Candidate application history

### 🔐 Security

* Password hashing
* JWT authentication
* Protected routes
* Role-based access control
* Environment-based configuration

### 🧪 Quality

* Automated tests
* Test coverage
* Database migrations
* CI/CD
* Dockerized development environment

> 🚧 Features are being implemented progressively throughout the project.

---

# 🛠️ Tech Stack

| Technology     | Purpose              |
| -------------- | -------------------- |
| Python         | Programming Language |
| FastAPI        | REST API Framework   |
| SQLAlchemy     | ORM                  |
| PostgreSQL     | Relational Database  |
| Alembic        | Database Migrations  |
| Pydantic       | Data Validation      |
| JWT            | Authentication       |
| Argon2         | Password Hashing     |
| Docker         | Containerization     |
| Docker Compose | Local Infrastructure |
| Pytest         | Testing              |
| GitHub Actions | CI/CD                |
| DataGrip       | Database Management  |

---

# 🏗️ Architecture

The project follows a modular backend architecture designed to separate API endpoints, business logic, database models, and validation.

```text
app/
├── core/          # Configuration, security and authentication
├── database/      # Database engine and session management
├── models/        # SQLAlchemy models
├── routers/       # API endpoints
├── schemas/       # Pydantic schemas
├── services/      # Business logic
└── main.py        # FastAPI application
```

---

# 🗄️ Database Architecture

The initial database model is based around users, companies, jobs, and applications.

```text
User
 │
 ├───────────────┐
 │               │
 ▼               ▼
Application    CompanyMember
 │               │
 │               ▼
 ▼             Company
Job              │
 ▲               │
 └───────────────┘
```

### Current User Model

```text
User
├── id
├── username
├── email
├── password
├── name
├── phone_number
├── role
├── created_at
└── updated_at
```

### Planned Entities

```text
Company
├── id
└── name

CompanyMember
├── id
├── role
├── salary
├── user_id
└── company_id

Job
├── id
├── title
├── content
└── company_id

Application
├── id
├── cv
├── letter
├── info
├── user_id
└── job_id
```

The database schema will evolve through **Alembic migrations** rather than manually modifying the PostgreSQL database.

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/MiguelP0rtela/job-application-tracker.git
cd job-application-tracker
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
POSTGRES_USER=jobtracker
POSTGRES_PASSWORD=your_password
POSTGRES_DB=job_tracker

DATABASE_URL=postgresql://jobtracker:your_password@localhost:5432/job_tracker
```

> Never commit `.env` or real credentials to the repository.

---

# 🐳 Running PostgreSQL

Start the PostgreSQL container:

```bash
docker compose up -d postgres
```

Check running containers:

```bash
docker ps
```

The PostgreSQL database will be available on:

```text
localhost:5432
```

---

# 🗃️ Database Migrations

The project uses **Alembic** for database schema management.

Create a new migration:

```bash
alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

Check the current migration:

```bash
alembic current
```

---

# ⚡ Running the API

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### Swagger

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

# 📡 Planned API

## Authentication

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| POST   | `/auth/register` | Register a user       |
| POST   | `/auth/login`    | Authenticate user     |
| POST   | `/auth/refresh`  | Refresh access token  |
| POST   | `/auth/logout`   | Revoke authentication |

---

## Users

| Method | Endpoint             | Description      |
| ------ | -------------------- | ---------------- |
| GET    | `/users/me`          | Get current user |
| PATCH  | `/users/me`          | Update profile   |
| PATCH  | `/users/me/password` | Change password  |

---

## Companies

| Method | Endpoint          | Description    |
| ------ | ----------------- | -------------- |
| POST   | `/companies`      | Create company |
| GET    | `/companies/{id}` | Get company    |
| PATCH  | `/companies/{id}` | Update company |
| DELETE | `/companies/{id}` | Delete company |

---

## Jobs

| Method | Endpoint     | Description |
| ------ | ------------ | ----------- |
| POST   | `/jobs`      | Create job  |
| GET    | `/jobs`      | List jobs   |
| GET    | `/jobs/{id}` | Get job     |
| PATCH  | `/jobs/{id}` | Update job  |
| DELETE | `/jobs/{id}` | Delete job  |

---

## Applications

| Method | Endpoint             | Description          |
| ------ | -------------------- | -------------------- |
| POST   | `/applications`      | Apply to a job       |
| GET    | `/applications`      | List applications    |
| GET    | `/applications/{id}` | Get application      |
| PATCH  | `/applications/{id}` | Update application   |
| DELETE | `/applications/{id}` | Withdraw application |

> API endpoints are subject to change as the application architecture evolves.

---

# 🧪 Testing

The project will use **Pytest** for automated testing.

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

The testing strategy will cover:

* User registration
* Authentication
* Authorization
* Company management
* Job management
* Job applications
* Validation
* Database interactions
* Protected endpoints
* Role-based permissions

---

# 🔄 CI/CD

GitHub Actions will be used to automate the development workflow.

Planned pipeline:

```text
Push / Pull Request
        ↓
Install dependencies
        ↓
Start PostgreSQL
        ↓
Run migrations
        ↓
Run tests
        ↓
Generate coverage
        ↓
Code quality checks
```

Planned quality checks include:

* Pytest
* Coverage
* Ruff
* Mypy

---

# 📌 Project Status

| Feature                    | Status |
| -------------------------- | :----: |
| FastAPI project setup      |    ✅   |
| Virtual environment        |    ✅   |
| PostgreSQL                 |    ✅   |
| Docker PostgreSQL          |    ✅   |
| SQLAlchemy                 |    ✅   |
| Environment configuration  |    ✅   |
| Alembic                    |    ✅   |
| Initial database migration |    ✅   |
| User model                 |    ✅   |
| User schemas               |    ⏳   |
| User registration          |    ⏳   |
| Password hashing           |    ⏳   |
| JWT authentication         |    ⏳   |
| Refresh tokens             |    ⏳   |
| Protected routes           |    ⏳   |
| Role-based authorization   |    ⏳   |
| Company model              |    ⏳   |
| Company members            |    ⏳   |
| Job model                  |    ⏳   |
| Job management             |    ⏳   |
| Application model          |    ⏳   |
| Application management     |    ⏳   |
| Automated tests            |    ⏳   |
| Test coverage              |    ⏳   |
| GitHub Actions             |    ⏳   |
| Dockerized API             |    ⏳   |
| Deployment                 |    ⏳   |

---

# 🎯 Project Goals

The main goal of this project is to build a realistic full-stack application while applying production-oriented software engineering practices.

The project focuses on:

* REST API development
* Authentication and authorization
* Relational database design
* Database migrations
* Secure password handling
* Role-based access control
* Docker
* Automated testing
* CI/CD
* Clean and maintainable architecture
* Production deployment

---

# 🎓 Learning Objectives

This project is being developed to strengthen practical knowledge of:

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* REST API design
* JWT authentication
* Password hashing
* Role-based authorization
* Docker
* Database architecture
* Automated testing
* CI/CD
* Backend architecture
* Full-stack application development

---

# 🚀 Future Improvements

Potential future improvements include:

* 🔎 Advanced job search
* 🎯 Job recommendation system
* 📊 Application analytics
* 📈 Candidate dashboard
* 📬 Email notifications
* 📅 Interview scheduling
* 📎 Cloud file storage for CVs
* 🔐 Additional security hardening
* 🚦 Rate limiting
* 📊 Logging and monitoring
* 📈 Prometheus metrics
* ☁️ Cloud deployment
* 🤖 AI-assisted job matching

---

# 🤝 Author

**Miguel Portela**

### GitHub

https://github.com/MiguelP0rtela

### LinkedIn

https://www.linkedin.com/in/miguel-portela-helloworld/

---

# 📄 License

This project is licensed under the **MIT License**.

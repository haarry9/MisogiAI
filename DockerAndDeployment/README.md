# Restaurant-Menu System (Dockerized, Cloud DB, Production Ready)

## Overview
A modern, production-ready restaurant-menu system built with FastAPI, Celery, Redis, SQLAlchemy, and PostgreSQL. The system is fully containerized using Docker and Docker Compose, integrates with a cloud-hosted PostgreSQL database, and is ready for deployment on AWS EC2 or similar environments.

---

## Features
- **FastAPI** backend for RESTful APIs
- **Celery** for background task processing (worker & beat)
- **Redis** for caching and as Celery broker
- **Cloud PostgreSQL** (RDS/Supabase/Neon/etc.) with connection pooling & SSL
- **Alembic** for database migrations
- **Nginx** as reverse proxy/load balancer
- **Flower** for Celery monitoring
- **Docker Compose** for orchestration
- **Environment-based config** via `.env`
- **Production-ready Dockerfile** (multi-stage, uv, non-root, healthchecks)

---

## Project Structure
```
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core settings, config
│   ├── db/            # DB models, session, migrations
│   ├── schemas/       # Pydantic schemas
│   ├── crud/          # CRUD operations
│   ├── services/      # Business logic
│   └── celery_worker/ # Celery tasks
├── alembic/           # Alembic migrations
│   └── versions/
├── nginx/             # Nginx config
├── Dockerfile         # Multi-stage Docker build
├── docker-compose.yml # Service orchestration
├── pyproject.toml     # Python project & dependencies (uv)
├── .env.example       # Environment variable template
└── README.md          # This file
```

---

## Quick Start

1. **Clone the repo & copy env:**
   ```sh
   cp .env.example .env
   # Edit .env with your secrets and cloud DB info
   ```

2. **Build & start all services:**
   ```sh
   docker compose up --build
   ```

3. **Run Alembic migrations:**
   ```sh
   docker compose exec app alembic upgrade head
   ```

4. **Access services:**
   - API: http://localhost:8000
   - Flower: http://localhost:5555
   - Nginx: http://localhost/

---

## Cloud Database Setup
- Use AWS RDS, Supabase, Neon, or similar for PostgreSQL
- Update `DATABASE_URL` in `.env` with your cloud DB credentials
- Ensure SSL is enabled (`DATABASE_SSL_MODE=require`)

---

## Deployment (AWS EC2 Example)
- Launch EC2 instance (Ubuntu recommended)
- Install Docker & Docker Compose
- Clone repo, set up `.env`
- Open necessary ports (80, 443, 8000, 5555, etc.)
- Use `docker compose up -d` for production
- Set up logging, monitoring, and health checks

---

## Alembic Migrations
- Alembic is pre-configured for cloud DB
- Migration scripts in `alembic/versions/`
- Run migrations with `alembic upgrade head`

---

## Environment Variables
See `.env.example` for all required variables:
- Database, Redis, Celery, AWS, API keys, etc.

---

## Notes
- Uses `uv` for dependency management (see `pyproject.toml`)
- All containers run as non-root for security
- Nginx handles SSL termination and reverse proxy
- Flower provides Celery monitoring UI

---

## License
MIT
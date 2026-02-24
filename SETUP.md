# Setup Instructions

This guide will help you set up the Runtime Rush platform for development.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- pip (Python package manager)
- npm (Node package manager)

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Database Services

Start PostgreSQL and Redis using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432 (main database)
- PostgreSQL on port 5433 (test database)
- Redis on port 6379

### 3. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` if needed to match your local configuration.

### 4. Run Database Migrations

Apply the database schema:

```bash
alembic upgrade head
```

### 5. Build Sandbox Docker Image

Build the Docker image used for code execution:

```bash
docker build -f docker/Dockerfile.sandbox -t runtime-rush-sandbox:latest .
```

### 6. Start Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API documentation: http://localhost:8000/docs

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm start
```

The frontend will be available at http://localhost:3000

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Verify Installation

1. Check backend health: http://localhost:8000/health
2. Check frontend loads: http://localhost:3000
3. Run backend tests: `cd backend && pytest`

## Troubleshooting

### Database Connection Issues

If you get database connection errors:

1. Verify PostgreSQL is running: `docker ps`
2. Check connection string in `.env`
3. Ensure port 5432 is not in use by another service

### Redis Connection Issues

If Redis connection fails:

1. Verify Redis is running: `docker ps`
2. Check Redis URL in `.env`
3. Test connection: `redis-cli ping`

### Docker Issues

If sandbox execution fails:

1. Verify Docker daemon is running
2. Check if sandbox image exists: `docker images | grep runtime-rush-sandbox`
3. Rebuild image if needed: `docker build -f docker/Dockerfile.sandbox -t runtime-rush-sandbox:latest .`

## Next Steps

After setup is complete, you can:

1. Review the design document: `.kiro/specs/runtime-rush-platform/design.md`
2. Check the task list: `.kiro/specs/runtime-rush-platform/tasks.md`
3. Start implementing features according to the task plan

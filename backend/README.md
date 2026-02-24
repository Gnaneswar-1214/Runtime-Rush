# Runtime Rush Backend

FastAPI-based backend for the Runtime Rush competitive coding platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start PostgreSQL and Redis:
```bash
docker-compose up -d
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will run on http://localhost:8000

## Technologies

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Docker (for sandbox execution)
- Pytest + Hypothesis (testing)

# Runtime Rush Platform

A competitive coding challenge platform where participants debug and reconstruct fragmented code under time pressure.

## Project Structure

```
runtime-rush-platform/
├── backend/          # FastAPI backend
│   ├── app/          # Application code
│   ├── alembic/      # Database migrations
│   ├── docker/       # Docker configurations
│   └── tests/        # Test suite
├── frontend/         # React frontend
│   ├── src/          # Source code
│   └── public/       # Static assets
└── .kiro/            # Kiro specs
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start PostgreSQL and Redis:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

Backend runs on http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend runs on http://localhost:3000

## Technologies

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- Redis - Caching
- Docker - Code execution sandbox
- Pytest + Hypothesis - Testing

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- Monaco Editor - Code editor component

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Property-Based Tests
The project uses Hypothesis for property-based testing to validate correctness properties across randomized inputs.

## Development

See individual README files in `backend/` and `frontend/` directories for detailed development instructions.

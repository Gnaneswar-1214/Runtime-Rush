from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ Allowed origins
origins = [
    "http://localhost:3000",
    "https://runtime-rush.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ IMPORTANT: add /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(challenges_sqlite.router, prefix="/api/challenges", tags=["Challenges"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
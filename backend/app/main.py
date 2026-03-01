from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ CORS configuration (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://runtime-rush.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],   # ✅ MUST be "*"
    allow_headers=["*"],   # ✅ MUST be "*"
)

# ✅ Include routers
app.include_router(challenges_sqlite.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
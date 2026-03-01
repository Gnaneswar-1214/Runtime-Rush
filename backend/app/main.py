from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ CORS configuration (ALLOW VERCEL + LOCAL)
origins = [
    "http://localhost:3000",                 # local development
    "https://runtime-rush.vercel.app",       # your frontend (change if different)
    "https://*.vercel.app",                  # allow preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 TEMP: allow all to confirm fix
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(challenges_sqlite.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
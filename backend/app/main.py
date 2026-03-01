from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ Allow frontend domains
origins = [
    "http://localhost:3000",
    "https://runtime-rush.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # ← MUST be "*"
    allow_headers=["*"],      # ← MUST be "*"
    expose_headers=["*"],     # ← important for some browsers
)

# Routers
app.include_router(challenges_sqlite.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Runtime Rush API running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
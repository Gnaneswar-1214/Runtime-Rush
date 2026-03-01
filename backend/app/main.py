from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ Allowed origins
origins = [
    "http://localhost:3000",           # local development
    "https://runtime-rush.vercel.app", # ✅ your real frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(challenges_sqlite.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
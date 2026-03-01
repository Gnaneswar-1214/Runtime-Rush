from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ CORS configuration
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

# ✅ FORCE handle OPTIONS (fixes 405 permanently)
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str, request: Request):
    return Response(status_code=200)

# Routers
app.include_router(challenges_sqlite.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
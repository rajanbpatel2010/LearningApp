from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.auth import Token, User, authenticate_user, create_access_token, require_role
from app.routers.coaching import router as coaching_router
from app.routers.knowledge import router as knowledge_router
from app.routers.orchestration import router as orchestration_router
from app.routers.questions import router as question_router

app = FastAPI(title="Learning Coach API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(question_router)
app.include_router(knowledge_router)
app.include_router(orchestration_router)
app.include_router(coaching_router)


@app.get("/")
def serve_frontend() -> FileResponse:
    frontend_path = Path(__file__).resolve().parents[1] / ".." / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/login", response_model=Token)
def login(username: str, password: str) -> Token:
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token({"sub": user.username, "role": user.role})
    return Token(access_token=access_token)


@app.get("/auth/me", response_model=User)
def get_me(user: User = Depends(require_role("learner", "admin"))) -> User:
    return user


@app.get("/admin/ping")
def admin_ping(user: User = Depends(require_role("admin"))) -> dict[str, str]:
    return {"status": "ok", "role": user.role}

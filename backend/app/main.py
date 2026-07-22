from fastapi import Depends, FastAPI, HTTPException, status

from app.auth import Token, User, authenticate_user, create_access_token, require_role

app = FastAPI(title="Learning Coach API")


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

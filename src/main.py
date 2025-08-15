from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict

FRONTEND_DIR = Path(__file__).parent / "frontend"


app = FastAPI()


class UserProfile(BaseModel):
    email: str
    is_active: bool = True
    profile_id: str
    registered_at: str
    updated_at: str
    username: str
    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "email": "user@example.com",
            "is_active": True,
            "profile_id": "0",
            "registered_at": "2025-06-15T18:29:56+00:00",
            "updated_at": "2025-06-15T18:29:56+00:00",
            "username": "user123",
        }],
    })


@app.get("/users/me", response_model=UserProfile)
def mock_get_user_profile():
    mock_user_data = {
        "email": "user@example.com",
        "is_active": True,
        "profile_id": "0",
        "registered_at": "2025-06-15T18:29:56+00:00",
        "updated_at": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return JSONResponse(content=mock_user_data, status_code=200)


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)

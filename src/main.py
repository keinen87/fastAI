from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).parent / "frontend"


app = FastAPI()


@app.get("/users/me")
def mock_get_user():
    mock_user_data = {
        "profileId": 0,
        "email": "user@example.com",
        "username": "string",
        "registeredAt": "string",
        "updatedAt": "string",
        "isActive": True,
    }
    return JSONResponse(content=mock_user_data, status_code=200)


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)

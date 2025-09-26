import asyncio
from pathlib import Path
from typing import Annotated, Union

from fastapi import Body, FastAPI, Path as pth
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

FRONTEND_DIR = Path(__file__).parent / "frontend"


app = FastAPI()


class UserProfileResponse(BaseModel):
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


SiteTitle = Annotated[
    str,
    Field(min_length=4),
    Field(description="Название веб-страницы в поисковой выдаче и на вкладке браузера"),
]

mock_site_schema = {
    "created_at": "2025-06-15T18:29:56+00:00",
    "html_code_download_url": "https://ya.ru/",
    "html_code_url": "https://ya.ru/",
    "id": 1,
    "prompt": "Сайт любителей играть в домино",
    "screenshot_url": "https://ya.ru/",
    "title": "Фан клуб Домино",
    "updated_at": "2025-06-15T18:29:56+00:00",
}


class SiteSchemaResponse(BaseModel):
    created_at: str
    html_code_download_url: str
    html_code_url: str
    id: int
    prompt: str
    screenshot_url: str
    title: SiteTitle
    updated_at: str

    model_config = ConfigDict(json_schema_extra={
        "examples": [mock_site_schema],
    })


class SiteCreate(BaseModel):
    prompt: str
    title: Union[SiteTitle, None] = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "prompt": "Сайт любителей играть в домино",
                "title": "Фан клуб игры в домино",
            },
            {
                "prompt": "Сайт любителей играть в домино",
            },
        ],
    })


class SiteGenerate(BaseModel):
    prompt: str
    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "prompt": "Сайт любителей играть в домино",
        }],
    })


@app.get("/users/me", response_model=UserProfileResponse, summary="Получить учётные данные пользователя")
def mock_get_user_profile():
    mock_user_schema = {
        "email": "user@example.com",
        "is_active": True,
        "profile_id": "0",
        "registered_at": "2025-06-15T18:29:56+00:00",
        "updated_at": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return JSONResponse(content=mock_user_schema, status_code=200)


@app.post("/sites/create", response_model=SiteSchemaResponse, summary="Создать сайт")
def create_site(site_data: SiteCreate):
    return JSONResponse(content=mock_site_schema, status_code=200)


async def get_mock_site():
    block_size = 1024
    seconds = 3
    with open("index.html", encoding="utf8") as file:
        while chunk := file.read(block_size):
            await asyncio.sleep(seconds)
            yield chunk


@app.post("/sites/{site_id}/generate",
          summary="Сгенерировать HTML код сайта",
          description="Код сайта будет транслироваться стримом по мере генерации.")
async def generate_site(site_id: int = pth(..., gt=0, title="ID сайта",
                        description="Должен быть положительным"),
                        site_data: SiteGenerate = Body(...)):
    return StreamingResponse(
        content=get_mock_site(),
        media_type="text/html",
    )


@app.get("/sites/my",
         response_model=SiteSchemaResponse,
         summary="Получить список сгенерированных сайтов текущего пользователя")
def mock_get_my_site():
    return JSONResponse(content=mock_site_schema, status_code=200)


@app.get("/sites/{site_id}", response_model=SiteSchemaResponse, summary="Получить сайт")
def get_user(site_id: int = pth(..., gt=0, title="ID сайта", description="Должен быть положительным")):
    return JSONResponse(content=mock_site_schema, status_code=200)


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)

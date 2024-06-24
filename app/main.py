import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers = [
        logging.StreamHandler()
    ]
)


app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "localhost:5173",
    "https://crm-xi-eight.vercel.app/"]

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include routers
from api.v1.endpoints import auth, user

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def index():
    return {"message":"hello world"}


register_tortoise(
    app=app,
    db_url=settings.DATABASE_URL,
    modules={"models": [
                "db.models.user",
                "db.models.admin",
        ]},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=11000, reload=True)
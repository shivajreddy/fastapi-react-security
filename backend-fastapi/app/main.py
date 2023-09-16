from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import connect_mongodb
from app.router.auth import router as auth_router

app = FastAPI(
    title="FastAPI-Security",
    description="""This project has all security features to be copied into a new project.
    It is JWT tokens, and all dependencies can be installed from requirements.txt
    """,
    version="1.0.0",
    contact={
        "name": "Shiva Reddy",
        "url": "https://github.com/shivajreddy"
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt"
    }
)

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    connect_mongodb()       # connect to database
    app.include_router(auth_router)     # include router's


@app.get("/api/healthchecker")
def root():
    return {"message": "Hello World"}


# TODO: delete these later
@app.get("/data")
def test_data():
    return {"some": "data"}

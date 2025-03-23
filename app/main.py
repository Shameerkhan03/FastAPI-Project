# uvicorn app.main:app --reload --> to run server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import vote
from . import models
from .database import engine
from .routers import post, user, auth

# this command is for sqlalchemy so we commenting it out, since we now have alembic we don't need it
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# either we can list down all the domains which we want to allow to talk to our API (like 'https://www.google.com') or we can add '*' to allow every domain
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# reference to router variables in routers files
# it will now check for all the path operations in each router and match the query with user input
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello Hello Hello World!!!!!"}

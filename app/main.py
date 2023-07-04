from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
# models.Base.metadata.create_all(bind=engine) # helps while not applying Alembic
from . import models,schemas,utils
from .router import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("ERROR:=>",error)
#         time.sleep(2)

my_posts = [
    {"id":1,"title":"first post title","content":"first post content"},
    {"id":2,"title":"second post title","content":"second post content"}
]

def findPost(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def findPostIndex(id):
    for index,post in enumerate(my_posts):
        if post["id"] == id:
            return index

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "hello world"}
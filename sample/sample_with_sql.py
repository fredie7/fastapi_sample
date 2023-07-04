from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[set] = None
    # id:int
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connection to database failed")
        print("ERROR:=>",error)
        time.sleep(2)

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

@app.get("/")
def root():
    return {"message": "hello world"}

@app.get("/posts")
def getPosts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.post("/posts/{id}")
def getPost(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    print(post)
    return {"post":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletPost(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def updatePost(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts with id {id} does not exist")
    return {"data": post}
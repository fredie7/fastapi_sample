from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # published: bool = True
    # rating: Optional[set] = None
    # id:int

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
    return {"data":my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    post = post.dict()
    post["id"] = randrange(0,1000000)
    my_posts.append(post)
    print(post)
    return {"data": post}

@app.post("/posts/{id}")
def getPost(id: int):
    post = findPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    print(post)
    return {"post":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletPost(id: int):
    postIndex = findPostIndex(id)
    # if postIndex == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    my_posts.pop(postIndex)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def updatePost(id:int, post:Post):
    postIndex = findPostIndex(id)
    if postIndex == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts with id {id} does not exist")
    post = post.dict()
    post["id"] = id
    my_posts[postIndex] = post
    return {"data": post}
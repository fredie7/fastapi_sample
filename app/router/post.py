from .. import models,schemas,utils,oauth2
from fastapi import Depends,status,FastAPI,Response,HTTPException,Depends,APIRouter
from typing import List,Optional
from sqlalchemy.orm import Session
from ..database import engine,get_db
from sqlalchemy import func

router = APIRouter(
    tags=["posts"]
)
# router = APIRouter(prefix="/posts")


# @router.get("/posts",response_model=List[schemas.Post])
@router.get("/posts",response_model=List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int= 10,skip: int= 0,search: Optional[str] = ""):
# def getPosts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int= 10,skip: int= 0):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # FOR LOGGED IN USER
    
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
    

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user)
    # print(current_user.id)
    # post = models.Post(owner_id=current_user.id,**post.dict())
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    # try:
    #     print(curent_user)
    #     post = models.Post(owner_id=curent_user.id,**post.dict())
    #     db.add(post)
    #     db.commit()
    #     db.refresh(post)
    #     return post
    # except Exception as e:
    #     print(e)
    # return post

# @router.post("/posts/{id}", response_model=schemas.Post)
@router.post("/posts/{id}", response_model=schemas.PostOut)
def getPost(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletPost(id: int, db: Session=Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def updatePost(id:int, updated_post:schemas.PostCreate, db: Session=Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
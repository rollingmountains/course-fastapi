from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=['posts'])



#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.ResponseOut])
def get_posts(db: Session = Depends(get_db), get_user = Depends(oauth2.get_current_user), limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.owner_id == get_user.id)

   # fetch_posts = posts.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Post.id).label('votes')).join(models.Vote, models.Post.id == models.Vote.posts_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not results :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts founds.") 

    return results




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), get_user = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=get_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.ResponseOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), get_user = (Depends(oauth2.get_current_user))):
    #get_post = db.query(models.Post).filter(models.Post.id == id).first()


    get_results = db.query(models.Post, func.count(models.Post.id).label("votes"), models.Post.owner_id.label("owner_id")).join(models.Vote, models.Post.id == models.Vote.posts_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if get_results == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found." )

    if get_user.id != get_results.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")
    return get_results

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    remove_post = post.first()


    #return {"data": 'successfully deleted'}

    if remove_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found.")

    if get_user.id != remove_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized to perform the action.")

    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)   

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, new_post: schemas.CreatePost, db: Session = Depends(get_db), get_user: int=(Depends(oauth2.get_current_user))):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s returning *""", (post.title, post.content, post.published, (id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    query_data = post_query.first()

    if query_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found.")

    if get_user.id != query_data.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized to perform the action.")

    post_query.update(new_post.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()

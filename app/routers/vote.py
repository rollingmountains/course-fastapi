from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from .. import models

router = APIRouter(prefix="/votes", tags=['votes'])


@router.post("/", status_code=status.HTTP_200_OK)
def create_votes(vote: schemas.VoteData, db: Session=Depends(get_db), get_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {vote.post_id} doesn't exist.")


    vote_query = db.query(models.Vote).filter(models.Vote.posts_id==vote.post_id, models.Vote.users_id == get_user.id)
    vote_found = vote_query.first()

    if vote.vote_direction==1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Sorry! User {get_user.id} has already voted on post {vote.post_id}" ) 
        new_vote = models.Vote(posts_id=vote.post_id, users_id=get_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": f"User {get_user.id} has successfully voted on post {vote.post_id}"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry, post {vote.post_id} does not exist.")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": f"User {get_user.id} has successfully removed vote from post {vote.post_id}"}
            



"""
@router.delete("/", status_code=status.HTTP_200_OK)
def create_votes(post: schemas.VoteData, db: Session=Depends(get_db), get_user=Depends(oauth2.get_current_user)):
    post_id = int(post.post_id)
    user_id = int(get_user.id)

    query = db.query(models.Vote).filter(models.Vote.posts_id == post.post_id)
    vote = query.first()


    if post.vote_direction == 0 and vote:
        .delete

    new_vote = models.Vote(posts_id=post_id, users_id=user_id)

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)


    return new_vote
"""
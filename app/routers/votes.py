from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..import schemas,database,models,oauth2

router=APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Votes,db:Session=Depends(database.get_db),user_id:int=Depends(oauth2.get_current_user)):
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==user_id.id)

    found_vote=vote_query.first()

    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {user_id.id} has already voted on post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote doesn't exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully delete vote"}


        
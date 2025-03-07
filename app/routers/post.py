from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import engine,get_db

router=APIRouter(
    tags=["Post"]
)

@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    ##python + sql

    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()


    #orm and sqlalchemy (no sql)

    # posts=db.query(models.Post).filter(models.Post.owner_id==user_id.id)
    # posts=db.query(models.Post).all()

    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).all()
    return posts



@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):

    #python + sql

    # cursor.execute(""" INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """ ,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    #orm and sql alchemy
    new_post=models.Post(owner_id=user_id.id,**post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


    ## in list (python and some logi)
    # post_dict=post.dict()
    # post_dict["id"]=randrange(1,1000000)
    # my_posts.append(post_dict)



@router.get("/posts/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    #python + sql

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id))) 
    # post=cursor.fetchone() 

    #sqlalchemy

    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found ")
    
    # if post.owner_id!=user_id.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to do the requested action")

    return post



@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    #python +sql

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """ ,(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()


    # sqlalchemy
    post_query=db.query(models.Post).filter(models.Post.id == id)

    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    
    if post.owner_id!=user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to do the requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),user_id:str=Depends(oauth2.get_current_user)):  
    #python + sql

    # cursor.execute(""" UPDATE posts SET title = %s ,content = %s,published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()

    #sqlalchemy
    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    
    if post.owner_id!=user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to do the requested action")

        
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()

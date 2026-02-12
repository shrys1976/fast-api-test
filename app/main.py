

from typing import Optional, List
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import model, schemas
from .database import engine, get_db




from starlette.status import HTTP_404_NOT_FOUND
model.Base.metadata.create_all(bind = engine)
app = FastAPI()

# dependency
 


    

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='py-api-test',
            user='postgres',
            password='shrys',
            cursor_factory=RealDictCursor,# gives column name when returning data
        )
        cursor = conn.cursor()
        print("db connected successfully")
        break  # exit loop once connection is successful
    except Exception as error:
        print("db connection failed")
        print("Error", error)
        time.sleep(2)  # wait before retrying to avoid tight loop



my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite pizza in nyc", "content": "Sam's pizza", "id": 2},
]    

def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i



@app.get("/") # endpoint for api , use http methods (CRUD)
def root():
    return {"message" : "Test"}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(model.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db=Depends(get_db)):
   # print(**post.model_dump()) # ** -> unpacks dictionary
    new_post = model.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""",
    #                     (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data":new_post}

  #  post_dict = post.model_dump()
  #  post_dict['id'] = randrange(0,1000000)
  #  my_posts.append(post_dict)
  #  return {"data":post_dict}



@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db=Depends(get_db)):
   # print(id)
#    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
#    post =  cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    # print(post)

    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
        detail = f"post with id {id} was not found")
    return post
        #response.status_code = status.HTTP_404_NOT_FOUND




@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail":post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db=Depends(get_db)) :

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit() # anytime we make a change to the db we need to commit

    post = db.query(model.Post).filter(model.Post.id == id)

    if post.first() ==None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} does not exist")

    
    post.delete(synchronize_session  = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db=Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title,post.content, post.published))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(model.Post).filter(model.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()
    

# @app.get("/sqlalchemy")
# def test_posts(db=Depends(get_db)):
#     posts = db.query(model.schemas.Post).all()
#     return {"status": "success", "data": posts}

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db=Depends(get_db)):
    new_user = model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at,
    }
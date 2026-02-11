
from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from .database import engine, get_db




from starlette.status import HTTP_404_NOT_FOUND
model.Base.metadata.create_all(bind = engine)
app = FastAPI()

# dependency
 


class Post(BaseModel):
    title: str
    content : str
    published : bool  = True
    

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


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db=Depends(get_db)):

    print(**post.model_dump()) # ** -> unpacks dictionary
    new_post = model.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""",
    #                     (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data":new_post}

  #  post_dict = post.model_dump()
  #  post_dict['id'] = randrange(0,1000000)
  #  my_posts.append(post_dict)
  #  return {"data":post_dict}



@app.get("/posts/{id}") 
def get_post(id:int, response: Response):
   # print(id)
   cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
   post =  cursor.fetchone()
  

   if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
        detail = f"post with id {id} was not found")
   return {"Post detail" : post} 
        #response.status_code = status.HTTP_404_NOT_FOUND




@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail":post}



@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit() # anytime we make a change to the db we need to commit

    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} does not exist")
   
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id:int,post:Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    (post.title,post.content, post.published))
   
    updated_post = cursor.fetchone()
    conn.commit()
    

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  # pyright: ignore[reportUnreachable]
        detail = f"post with id: {id} does not exist")
    
    return {"data" : updated_post}
    

@app.get("/sqlalchemy")
def test_posts(db=Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"status": "success", "data": posts}

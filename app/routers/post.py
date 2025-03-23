from .. import models, schemas, oauth2
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", tags=["Posts"]
)  # tags creates a heading of 'Posts' on the SwaggerUI page


# order matters. if same url has multiple path operations it will use the first one
# @app.get("/")
# def get_posts():
#     return {"data": "There are your posts"}


# post method is used to send data to api server
# @app.post("/createposts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}


# @app.post("/posts")
# def create_post(post: Post):
#     print(post)
#     print(post.dict()) #same output like above but in dictionary
#     return {"data": post}


# C of CRUD that is Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # "current_user: int = Depends(oauth2.get_current_user)", this dependency verifies if the user is loggedin before he can perform CRUD operations
    # We could've used f-string formatting to add the variables but we used %s to be able to sanitize the input
    # if the user inputs a sql query in the content it could manipulate our database, this is known as sql injection attack
    # using %s and passing another parameter for variables validates the input before adding to database
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title,
    #                 post.content, post.published))
    # new_post = cursor.fetchone() #this is gonna fetch the output of returning query
    # conn.commit() #  even if we create a post successfully without this no changes will be made to the database

    new_post = models.Post(
        owner_id=current_user.id, **post.dict()
    )  # unpacks the user input stored in a dict

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Like RETURNING * in SQL

    return new_post


# Above specific id
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return post


# R of CRUD that is Read (specific id)
"""parameter is gonna validate if id can be converted to int and then convert it in int. 
if cant be converted then will throw error because /posts/id here id will always be integer"""


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # id: int explanation above
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id))) #widout str() it will throw error bcoz select statement is a str, id must also be str
    # post = cursor.fetchone()

    # 'filter' is like a WHERE in SQL and w/o .first() the line is just a raw query, won't execute. first() returns the 1st post that matches id
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        # do this
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )
        # or this
        # response.status = status.HTTP_404_NOT_FOUND
        # return {f"message": f"Post with {id} was not found"}
        # or this
        # response.status_code = 404
    return post


# R of CRUD that is Read (all posts)
@router.get(
    "/", response_model=List[schemas.PostOut]
)  # to access this user has to access post section of our url eg google.com/posts
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    # equivalent to this sql query (with features of search filtering)
    # Select posts.id, COUNT(votes.post_id) from posts
    # left join votes
    # on posts.id = votes.post_id
    # group by posts.id
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return results

    # if we want to retrieve only the posts that the loggedin user made, we do this:
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()


"""Now if user tries to access this url "/posts/latest" it will the server would start matching
the url in all decorators one by one and when it reaches "/posts/{id}" it will think that it is 
trying to reach it but with str in place of id so it will throw error regarding that issue. it will be 
confusing to understand the error at that time so We have to remember that it the server checks decorator
from top to bottom, so we'll place latest decorator above {id} so that if latest is written in the url
it catches that first."""
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} doesn't exist",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

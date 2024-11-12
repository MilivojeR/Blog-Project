from datetime import datetime
from typing import Annotated, Optional, List
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
import crud.posts as posts
from crud.tags import delete_unused_tags
from exceptions import DbnotFoundException
from schemas.posts import FilterPosts, Post, PostCreate, PostUpdate, PostUpdatePATCH, PostUpdatePUT, PostFilter
from database import db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[Post])
def list_posts(db: db, filters: Annotated[FilterPosts, Query()]):
    return posts.list_posts(db, filters)


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: db):
    try:
        return posts.get_post(db, post_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.post("", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: db):
    post = posts.create_post(db, post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, post: PostUpdate, db: db, background_tasks: BackgroundTasks):
    try:
        post = posts.update_post(db, post_id, post)
        db.commit()
        db.refresh(post)
        background_tasks.add_task(delete_unused_tags, db)
        return post
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: db, background_tasks: BackgroundTasks):
    try:
        posts.delete_post(db, post_id)
        db.commit()
        background_tasks.add_task(delete_unused_tags, db)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")
    
    
@router.put("/posts/{post_id}", response_model=Post)
def update_post_put_route(post_id: int, post_data: PostUpdatePUT, db: db, background_tasks: BackgroundTasks):
    post = update_post_put_route(db, post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    background_tasks.add_task(delete_unused_tags, db)
    return post

@router.patch("/posts/{post_id}", response_model=Post)
def update_post_patch_route(post_id: int, post_data:PostUpdatePATCH, db: db, background_tasks: BackgroundTasks):
    post =  update_post_patch_route(db, post_data, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    background_tasks.add_task(delete_unused_tags, db)
    return post

@router.get("/posts")
def read_posts(db: db, section_id: int, tags: List[str] = Query([]), created_at_gt: Optional[datetime] = Query(None), created_at_lt: Optional[datetime] = Query(None)):
    filters = PostFilter(
        section_id=section_id,
        tags=tags,
        created_at_gt=created_at_gt,
        created_at_lt=created_at_lt
    )
    return posts.get_filtered_posts(db, filters)


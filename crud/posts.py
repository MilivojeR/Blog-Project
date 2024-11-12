from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from crud.sections import get_section
from crud.tags import delete_unused_tags, get_or_create_tags
from exceptions import DbnotFoundException
from models.posts import Post
from models.tags import Tag
from schemas.posts import FilterPosts, PostCreate, PostFilter, PostUpdate, PostUpdatePATCH, PostUpdatePUT


def get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise DbnotFoundException
    return post


def list_posts(db: Session, filters: Optional[FilterPosts] = None) -> list[Post]:
    query = select(Post)

    if filters:
        if filters.title:
            query = query.where(Post.title.ilike(f"%{filters.title}%"))

        # Add more filters

    return db.scalars(query).all()


def create_post(db: Session, post_data: PostCreate) -> Post:
    section = get_section(db, post_data.section_id)

    new_post = Post(**post_data.model_dump(exclude={"tags"}))
    new_post.section = section

    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        new_post.tags = tags

    db.add(new_post)
    return new_post


def update_post(db: Session, post_id: int, post_data: PostUpdate) -> Post:
    post_being_updated = get_post(db, post_id)

    update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})

    for key, value in update_data.items():
        setattr(post_being_updated, key, value)

    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        post_being_updated.tags = tags

    return post_being_updated


def delete_post(db: Session, post_id: int) -> None:
    post = get_post(db, post_id)
    db.delete(post)
    delete_unused_tags(db)


def update_post_put(db: Session, post_id: int, post_data:PostUpdatePUT):
    post = db.query(Post).filter(post.id == post_id).first()
    if not post:
        return  None
    post.title = post_data.title
    post.body = post_data.body
    post.section_id = post_data.section_id
    post.tags = post_data.tags
    delete_unused_tags(db)
    return post

def update_post_patch(db: Session, post_id: int, post_data=PostUpdatePATCH):
    post = db.query(Post).filter(post.id == post_id).first()
    if not post:
        return None
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.body is not None:
        post.body = post_data.body
    if post_data.section_id is not None:
        post.section_id = post_data.section_id
    if post_data.tags is not None:
        post.tags = post_data.tags
    delete_unused_tags(db)
    return post

def get_filtered_posts(db: Session, filters: PostFilter):
    query = db.query(Post)

    #filters by section
    if filters.section_id:
        query = query.filter(Post.section_id == filters.section_id)

    #filters by tags
    if filters.tags:
        for tag_name in filters.tags:
            query = query.filter(Post.tags.any(Tag.name == tag_name))
        
    #filter by created date
    if filters.created_at_gt:
        query= query.filter(Post.created_at > filters.created_at_gt)
    if filters.created_at_lt:
        query = query.filter(Post.created_at < filters.created_at_lt)

    return query.all()

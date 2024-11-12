from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from crud.tags import get_tags_with_post_count
from schemas.tags import TagsWithPostCount
from database import db

@router.get("/tags", response_model = list[TagsWithPostCount])
def read_tags(db:db):
    return get_tags_with_post_count(db)
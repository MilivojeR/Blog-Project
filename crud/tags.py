from sqlalchemy import select, func
from models.tags import Tag, post_tags
from sqlalchemy.orm import Session
from schemas.tags import TagsWithPostCount


def get_or_create_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    unique_tag_names = list(set(tag_names))

    # Step 1: Retrieve existing Tags from the db
    existing_tags_query = select(Tag).where(Tag.name.in_(unique_tag_names))
    existing_tags = db.scalars(existing_tags_query).all()

    existing_tag_names = {tag.name for tag in existing_tags}

    # Step 2:  identifiy tag names to be created
    new_tag_names = set(unique_tag_names) - existing_tag_names
    new_tags = [Tag(name=name) for name in new_tag_names]  # list comprehension

    # new_tags = []
    # for name in new_tag_names:
    #     tag = Tag(name=name)
    #     new_tags.apend(tag)

    db.add_all(new_tags)
    return existing_tags + new_tags


def get_tags_with_post_count(db: Session):
    # Query to get each tag with the count of associated posts
    tag_counts = db.query(
        Tag.id,
        Tag.name,
        func.count(post_tags.c.post_id).label("posts_count")
    ).join(post_tags, Tag.id == post_tags.c.tag_id, isouter=True) \
     .group_by(Tag.id) \
     .all()
    

    return [TagsWithPostCount(id=tag.id, name=tag.name, post_count=tag.post_count) for tag in tag_counts]


def delete_unused_tags(db: Session):
    unused_tags = db.query(Tag).outerjoin(post_tags, Tag.id == post_tags.c.tag_id).group_by(Tag.id).having(func.count(post_tags.c.post_id) == 0).all()

    for tag in unused_tags:
        db.delete(tag)
        
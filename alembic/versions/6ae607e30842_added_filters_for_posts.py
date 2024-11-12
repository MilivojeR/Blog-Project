"""Added filters for Posts

Revision ID: 6ae607e30842
Revises: 689795869860
Create Date: 2024-11-12 14:00:19.124371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ae607e30842'
down_revision: Union[str, None] = '689795869860'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('tags')
    op.drop_table('post_tags')
    op.drop_table('sections')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sections',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('post_tags',
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.Column('tag_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('body', sa.TEXT(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('section_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

"""add_bingo

Revision ID: e8ef753e6b86
Revises: 13fddd167a33
Create Date: 2024-03-02 13:09:02.770148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8ef753e6b86'
down_revision: Union[str, None] = '13fddd167a33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bingo_interaction',
    sa.Column('interaction_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('send_user_id', sa.Integer(), nullable=False),
    sa.Column('receive_user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('interaction_id')
    )
    op.create_table('meta_word',
    sa.Column('word_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word_type', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('word_id')
    )
    op.create_table('user_word_status',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('user_id', 'word_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_word_status')
    op.drop_table('meta_word')
    op.drop_table('bingo_interaction')
    # ### end Alembic commands ###

"""init

Revision ID: 0d062271949e
Revises: 
Create Date: 2022-12-12 14:58:53.706106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d062271949e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('policy', sa.Boolean(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=False),
    sa.Column('subscription', sa.Enum('FREE', 'PREMIUM', name='subscriptionlevel'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('quiz',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('type', sa.Enum('SURVEY', 'TEST', name='quiztype'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('question',
    sa.Column('quiz_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('file', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('SINGLE', 'MULTIPLE', name='questiontype'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('quiz_id')
    )
    op.create_table('ans_option',
    sa.Column('question_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('file', sa.String(), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('question_id', 'id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('question_id')
    )
    op.create_table('quiz_result',
    sa.Column('quiz_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('question_id', sa.UUID(), nullable=False),
    sa.Column('solution', sa.JSON(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'user_id', 'question_id', 'id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('question_id'),
    sa.UniqueConstraint('quiz_id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz_result')
    op.drop_table('ans_option')
    op.drop_table('question')
    op.drop_table('quiz')
    op.drop_table('users')
    # ### end Alembic commands ###
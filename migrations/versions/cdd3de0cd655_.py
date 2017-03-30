"""empty message

Revision ID: cdd3de0cd655
Revises: 
Create Date: 2017-03-30 11:31:04.016799

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision = 'cdd3de0cd655'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('areas_of_interest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True),
    sa.Column('centroid', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('mapping_level', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('aoi_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('default_locale', sa.String(length=10), nullable=True),
    sa.Column('author_id', sa.BigInteger(), nullable=False),
    sa.Column('mapper_level', sa.Integer(), nullable=False),
    sa.Column('enforce_mapper_level', sa.Boolean(), nullable=True),
    sa.Column('enforce_validator_role', sa.Boolean(), nullable=True),
    sa.Column('private', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['aoi_id'], ['areas_of_interest.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='fk_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_info',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('locale', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('short_description', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('instructions', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('project_id', 'locale')
    )
    op.create_index('idx_project_info composite', 'project_info', ['locale', 'project_id'], unique=False)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=False),
    sa.Column('y', sa.Integer(), nullable=False),
    sa.Column('zoom', sa.Integer(), nullable=False),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True),
    sa.Column('task_status', sa.Integer(), nullable=True),
    sa.Column('task_locked', sa.Boolean(), nullable=True),
    sa.Column('lock_holder_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['lock_holder_id'], ['users.id'], name='fk_users'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id', 'project_id')
    )
    op.create_index(op.f('ix_tasks_project_id'), 'tasks', ['project_id'], unique=False)
    op.create_table('task_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('action_text', sa.String(), nullable=True),
    sa.Column('action_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['task_id', 'project_id'], ['tasks.id', 'tasks.project_id'], name='fk_tasks'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_history_composite', 'task_history', ['task_id', 'project_id'], unique=False)
    op.create_index(op.f('ix_task_history_project_id'), 'task_history', ['project_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_history_project_id'), table_name='task_history')
    op.drop_index('idx_task_history_composite', table_name='task_history')
    op.drop_table('task_history')
    op.drop_index(op.f('ix_tasks_project_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index('idx_project_info composite', table_name='project_info')
    op.drop_table('project_info')
    op.drop_table('projects')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('areas_of_interest')
    # ### end Alembic commands ###
"""cascade del games

Revision ID: ab627dbe10ff
Revises: eba2c1b1c1ee
Create Date: 2025-06-20 15:55:17.396261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab627dbe10ff'
down_revision = 'eba2c1b1c1ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_games_user_id_users'), type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_games_user_id_users'), 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_games_user_id_users'), type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_games_user_id_users'), 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###

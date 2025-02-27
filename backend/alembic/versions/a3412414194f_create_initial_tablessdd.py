"""Create initial tablessdd

Revision ID: a3412414194f
Revises: 
Create Date: 2025-01-02 22:08:01.904557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3412414194f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('facebook_access_token', sa.String(), nullable=True),
    sa.Column('google_credentials', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_facebook_access_token'), 'users', ['facebook_access_token'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_user_email'), 'users', ['user_email'], unique=True)
    op.create_table('ad_accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.String(), nullable=False),
    sa.Column('channel', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ad_accounts_account_id'), 'ad_accounts', ['account_id'], unique=True)
    op.create_index(op.f('ix_ad_accounts_channel'), 'ad_accounts', ['channel'], unique=False)
    op.create_index(op.f('ix_ad_accounts_id'), 'ad_accounts', ['id'], unique=False)
    op.create_index(op.f('ix_ad_accounts_user_id'), 'ad_accounts', ['user_id'], unique=False)
    op.create_table('ad_campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ad_account_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ad_account_id'], ['ad_accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ad_campaigns_ad_account_id'), 'ad_campaigns', ['ad_account_id'], unique=False)
    op.create_index(op.f('ix_ad_campaigns_id'), 'ad_campaigns', ['id'], unique=False)
    op.create_table('ad_creatives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ad_campaign_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ad_campaign_id'], ['ad_campaigns.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ad_creatives_ad_campaign_id'), 'ad_creatives', ['ad_campaign_id'], unique=False)
    op.create_index(op.f('ix_ad_creatives_id'), 'ad_creatives', ['id'], unique=False)
    op.create_table('recommendations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ad_account_id', sa.Integer(), nullable=True),
    sa.Column('ad_campaign_id', sa.Integer(), nullable=True),
    sa.Column('ad_creative_id', sa.Integer(), nullable=True),
    sa.Column('recommendation_text', sa.Text(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ad_account_id'], ['ad_accounts.id'], ),
    sa.ForeignKeyConstraint(['ad_campaign_id'], ['ad_campaigns.id'], ),
    sa.ForeignKeyConstraint(['ad_creative_id'], ['ad_creatives.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recommendations_ad_account_id'), 'recommendations', ['ad_account_id'], unique=False)
    op.create_index(op.f('ix_recommendations_ad_campaign_id'), 'recommendations', ['ad_campaign_id'], unique=False)
    op.create_index(op.f('ix_recommendations_ad_creative_id'), 'recommendations', ['ad_creative_id'], unique=False)
    op.create_index(op.f('ix_recommendations_id'), 'recommendations', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_recommendations_id'), table_name='recommendations')
    op.drop_index(op.f('ix_recommendations_ad_creative_id'), table_name='recommendations')
    op.drop_index(op.f('ix_recommendations_ad_campaign_id'), table_name='recommendations')
    op.drop_index(op.f('ix_recommendations_ad_account_id'), table_name='recommendations')
    op.drop_table('recommendations')
    op.drop_index(op.f('ix_ad_creatives_id'), table_name='ad_creatives')
    op.drop_index(op.f('ix_ad_creatives_ad_campaign_id'), table_name='ad_creatives')
    op.drop_table('ad_creatives')
    op.drop_index(op.f('ix_ad_campaigns_id'), table_name='ad_campaigns')
    op.drop_index(op.f('ix_ad_campaigns_ad_account_id'), table_name='ad_campaigns')
    op.drop_table('ad_campaigns')
    op.drop_index(op.f('ix_ad_accounts_user_id'), table_name='ad_accounts')
    op.drop_index(op.f('ix_ad_accounts_id'), table_name='ad_accounts')
    op.drop_index(op.f('ix_ad_accounts_channel'), table_name='ad_accounts')
    op.drop_index(op.f('ix_ad_accounts_account_id'), table_name='ad_accounts')
    op.drop_table('ad_accounts')
    op.drop_index(op.f('ix_users_user_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_facebook_access_token'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

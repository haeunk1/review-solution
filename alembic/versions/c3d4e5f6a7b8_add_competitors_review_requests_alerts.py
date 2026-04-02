"""add competitors, review_requests, review_alerts tables

Revision ID: c3d4e5f6a7b8
Revises: b1c2d3e4f5a6
Create Date: 2026-04-02

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── competitors ──────────────────────────────────────────────────────────
    op.create_table(
        'competitors',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('store_id', sa.String(), sa.ForeignKey('stores.store_id'), nullable=False, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('platform', sa.String(), nullable=False),
        sa.Column('platform_place_id', sa.String(), nullable=False),
        sa.Column('address', sa.String()),
        sa.Column('avg_rating', sa.Float()),
        sa.Column('total_reviews', sa.Integer(), default=0),
        sa.Column('positive_keywords', sa.Text()),
        sa.Column('negative_keywords', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_collected_at', sa.DateTime(timezone=True)),
    )

    # ── competitor_reviews ───────────────────────────────────────────────────
    op.create_table(
        'competitor_reviews',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('competitor_id', sa.Integer(), sa.ForeignKey('competitors.id'), nullable=False, index=True),
        sa.Column('platform', sa.String(), nullable=False),
        sa.Column('platform_review_id', sa.String(), index=True),
        sa.Column('author', sa.String()),
        sa.Column('rating', sa.Float()),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('visited_date', sa.String()),
        sa.Column('sentiment', sa.String()),
        sa.Column('keywords', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── review_requests ──────────────────────────────────────────────────────
    op.create_table(
        'review_requests',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('store_id', sa.String(), sa.ForeignKey('stores.store_id'), nullable=False, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('target_platform', sa.String(), nullable=False),
        sa.Column('short_url', sa.String(), unique=True),
        sa.Column('qr_code_url', sa.String()),
        sa.Column('click_count', sa.Integer(), default=0),
        sa.Column('review_count', sa.Integer(), default=0),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── review_alerts ────────────────────────────────────────────────────────
    op.create_table(
        'review_alerts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('store_id', sa.String(), sa.ForeignKey('stores.store_id'), nullable=False, index=True),
        sa.Column('review_id', sa.Integer(), sa.ForeignKey('reviews.id'), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('is_resolved', sa.Boolean(), default=False),
        sa.Column('is_blacklist', sa.Boolean(), default=False),
        sa.Column('suggested_reply', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('review_alerts')
    op.drop_table('review_requests')
    op.drop_table('competitor_reviews')
    op.drop_table('competitors')

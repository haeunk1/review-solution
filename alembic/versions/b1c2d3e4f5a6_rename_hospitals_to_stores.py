"""rename hospitals to stores and drop gangnamunni

Revision ID: b1c2d3e4f5a6
Revises: 28791a120f43
Create Date: 2026-04-01

변경 내용:
- hospitals 테이블 → stores 로 RENAME
- hospitals.hospital_id 컬럼 → store_id 로 RENAME
- hospitals.category 컬럼 → business_type 으로 RENAME
- hospitals.gangnamunni_id 컬럼 DROP
- reviews.hospital_id 컬럼 → store_id 로 RENAME (FK 재설정)
- Platform enum 에서 gangnamunni 제거
"""
from alembic import op
import sqlalchemy as sa


revision = "b1c2d3e4f5a6"
down_revision = "28791a120f43"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. FK 제약조건 제거 (reviews → hospitals) — 실제 DB 제약명 fk_hospital
    op.drop_constraint("fk_hospital", "reviews", type_="foreignkey")

    # 2. reviews.hospital_id → store_id
    op.alter_column("reviews", "hospital_id", new_column_name="store_id")

    # 3. hospitals 테이블 컬럼 변경
    op.alter_column("hospitals", "hospital_id", new_column_name="store_id")
    op.alter_column("hospitals", "category", new_column_name="business_type")
    op.drop_column("hospitals", "gangnamunni_id")

    # 4. hospitals 테이블 → stores 로 RENAME
    op.rename_table("hospitals", "stores")

    # 5. 인덱스 재생성
    op.drop_index("ix_hospitals_hospital_id", table_name="stores")
    op.drop_index("ix_hospitals_tenant_id", table_name="stores")
    op.drop_index("ix_reviews_hospital_id", table_name="reviews")

    op.create_index("ix_stores_store_id", "stores", ["store_id"], unique=False)
    op.create_index("ix_stores_tenant_id", "stores", ["tenant_id"], unique=False)
    op.create_index("ix_reviews_store_id", "reviews", ["store_id"], unique=False)

    # 6. FK 제약조건 재생성 (reviews → stores)
    op.create_foreign_key(
        "reviews_store_id_fkey",
        "reviews", "stores",
        ["store_id"], ["store_id"],
    )

    # 7. Platform enum에서 gangnamunni 제거 (PostgreSQL)
    op.execute("ALTER TYPE platform RENAME TO platform_old")
    op.execute("CREATE TYPE platform AS ENUM ('naver', 'google')")
    op.execute(
        "ALTER TABLE reviews ALTER COLUMN platform "
        "TYPE platform USING platform::text::platform"
    )
    op.execute("DROP TYPE platform_old")


def downgrade() -> None:
    # Platform enum 복원
    op.execute("ALTER TYPE platform RENAME TO platform_old")
    op.execute("CREATE TYPE platform AS ENUM ('naver', 'google', 'gangnamunni')")
    op.execute(
        "ALTER TABLE reviews ALTER COLUMN platform "
        "TYPE platform USING platform::text::platform"
    )
    op.execute("DROP TYPE platform_old")

    # FK 제거
    op.drop_constraint("reviews_store_id_fkey", "reviews", type_="foreignkey")

    # 인덱스 복원
    op.drop_index("ix_reviews_store_id", table_name="reviews")
    op.drop_index("ix_stores_store_id", table_name="stores")
    op.drop_index("ix_stores_tenant_id", table_name="stores")

    op.create_index("ix_reviews_hospital_id", "reviews", ["hospital_id"], unique=False)

    # stores → hospitals 로 RENAME
    op.rename_table("stores", "hospitals")

    # 컬럼 복원
    op.alter_column("hospitals", "store_id", new_column_name="hospital_id")
    op.alter_column("hospitals", "business_type", new_column_name="category")
    op.add_column("hospitals", sa.Column("gangnamunni_id", sa.String(), nullable=True))

    op.create_index("ix_hospitals_hospital_id", "hospitals", ["hospital_id"], unique=False)
    op.create_index("ix_hospitals_tenant_id", "hospitals", ["tenant_id"], unique=False)

    # reviews 복원
    op.alter_column("reviews", "store_id", new_column_name="hospital_id")
    op.create_index("ix_reviews_hospital_id", "reviews", ["hospital_id"], unique=False)
    op.create_foreign_key(
        "reviews_hospital_id_fkey",
        "reviews", "hospitals",
        ["hospital_id"], ["hospital_id"],
    )

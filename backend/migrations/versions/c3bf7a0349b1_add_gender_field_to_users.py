"""add_gender_field_to_users

Revision ID: c3bf7a0349b1
Revises: f63c351e24a8
Create Date: 2025-08-22 14:19:34.447427

"""

import random
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c3bf7a0349b1"
down_revision: Union[str, Sequence[str], None] = "f63c351e24a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()

    # Check if the gender enum type already exists
    result = connection.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM pg_type 
            WHERE typname = 'gender'
        )
    """)
    )
    enum_exists = result.scalar()

    if not enum_exists:
        # Create the Gender enum type
        gender_enum = postgresql.ENUM(
            "MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY", name="gender"
        )
        gender_enum.create(connection)
        print("✅ Created gender enum type")
    else:
        # Drop and recreate the enum to ensure it has the correct values
        connection.execute(sa.text("DROP TYPE IF EXISTS gender CASCADE"))
        gender_enum = postgresql.ENUM(
            "MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY", name="gender"
        )
        gender_enum.create(connection)
        print("✅ Recreated gender enum type with correct values")

    # Check if the gender column already exists
    result = connection.execute(
        sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'User' AND column_name = 'gender'
    """)
    )
    column_exists = result.fetchone() is not None

    if not column_exists:
        # Add the gender column to the User table
        op.add_column(
            "User",
            sa.Column(
                "gender",
                sa.Enum("MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY", name="gender"),
                nullable=True,
            ),
        )
        print("✅ Added gender column to User table")
    else:
        # Drop and recreate the column to ensure it uses the correct enum type
        connection.execute(sa.text('ALTER TABLE "User" DROP COLUMN gender'))
        op.add_column(
            "User",
            sa.Column(
                "gender",
                sa.Enum("MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY", name="gender"),
                nullable=True,
            ),
        )
        print("✅ Recreated gender column with correct enum type")

    # Update existing users with random gender values
    # We'll use a deterministic approach based on user ID to ensure consistency

    # Get all users without gender
    result = connection.execute(
        sa.text('SELECT id, name, email FROM "User" WHERE gender IS NULL')
    )
    users = result.fetchall()

    if users:
        print(f"Found {len(users)} users without gender fields, updating...")

        # Define gender choices
        gender_choices = ["MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY"]

        for user in users:
            # Use user ID to deterministically assign gender
            # This ensures the same user always gets the same gender across different runs
            random.seed(user[0])  # Use user ID as seed
            gender = random.choice(gender_choices)

            # Update the user with the assigned gender
            connection.execute(
                sa.text('UPDATE "User" SET gender = :gender WHERE id = :user_id'),
                {"gender": gender, "user_id": user[0]},
            )
            print(f"  - Updated {user[1]} ({user[2]}) with gender: {gender}")

        print(f"✅ Successfully updated {len(users)} users with gender fields")
    else:
        print("✅ All users already have gender fields set")


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()

    # Check if the gender column exists before trying to drop it
    result = connection.execute(
        sa.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'User' AND column_name = 'gender'
    """)
    )
    column_exists = result.fetchone() is not None

    if column_exists:
        # Remove the gender column from the User table
        op.drop_column("User", "gender")
        print("✅ Removed gender column from User table")
    else:
        print("✅ Gender column does not exist in User table")

    # Check if the gender enum type exists before trying to drop it
    result = connection.execute(
        sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM pg_type 
            WHERE typname = 'gender'
        )
    """)
    )
    enum_exists = result.scalar()

    if enum_exists:
        # Drop the Gender enum type
        gender_enum = postgresql.ENUM(
            "MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY", name="gender"
        )
        gender_enum.drop(connection)
        print("✅ Removed gender enum type")
    else:
        print("✅ Gender enum type does not exist")

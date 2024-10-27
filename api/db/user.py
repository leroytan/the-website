from sqlmodel import Session, select
from db.models import User
from db.connection import engine
from exceptions import EmailAlreadyUsedError, EmailNotFoundError

def check_email_unused(email: str) -> None:
    with Session(engine) as session:
        # Check if the email already exists
        statement = select(User).where(User.email == email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise EmailAlreadyUsedError(email)


def create_user(email: str, name: str, password_hash: str, user_type: str) -> User:
    
    check_email_unused(email)

    # Step 1: Create a basic user entry with "tutor" as the user type
    new_user = User(
        email=email,
        name=name,
        password_hash=password_hash,
        user_type=user_type
    )

    # Step 2: Insert the user into the database
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Get the assigned user ID

    return new_user




def get_user_by_email(email: str) -> User:
    """Retrieve the hashed password for the given email."""
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user:
            raise EmailNotFoundError(email)

        return user


if __name__ == "__main__":
    # Example usage
    new_tutor = create_user(
        email="tutor@example.com",
        name="Alice Tutor",
        password_hash="hashed_password_here",
        user_type="tutor"
    )
    print(f"New tutor created: {new_tutor}")

    # Example usage
    try:
        hashed_password = get_password_hash_by_email("tutor@example.com")
        print(f"Password hash: {hashed_password}")
    except ValueError as e:
        print(e)

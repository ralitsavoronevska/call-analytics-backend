from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    user = db.scalar(statement)

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_user_token(user: User) -> str:
    return create_access_token(user.id)
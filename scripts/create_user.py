import argparse
import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User, UserRole


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an application user"
    )
    parser.add_argument("--email", required=True)
    parser.add_argument(
        "--role",
        required=True,
        choices=[role.value for role in UserRole],
    )

    args = parser.parse_args()
    email = args.email.strip().lower()

    if not email or "@" not in email:
        parser.error("Provide a valid email address.")

    password = getpass.getpass("Password: ")
    confirmation = getpass.getpass("Confirm password: ")

    if password != confirmation:
        parser.error("Passwords do not match.")

    if len(password) < 12:
        parser.error("Password must contain at least 12 characters.")

    with SessionLocal() as db:
        existing_user = db.scalar(
            select(User).where(User.email == email)
        )

        if existing_user is not None:
            parser.error("A user with this email already exists.")

        user = User(
            email=email,
            hashed_password=hash_password(password),
            role=UserRole(args.role),
        )

        db.add(user)
        db.commit()

        print(f"User created: {email} ({args.role})")


if __name__ == "__main__":
    main()
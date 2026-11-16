"""Create an administrator from a terminal with access to the backend database."""

import argparse
from getpass import getpass

from pydantic import ValidationError
from sqlalchemy import func, inspect, select
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models import order  # Registers the User.orders relationship.
from app.models.user import User
from app.schemas.user import UserCreate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    if not inspect(engine).has_table("users"):
        parser.exit(1, "Start the backend first to initialize the database.\n")

    password = getpass("Administrator password: ")
    if password != getpass("Confirm password: "):
        parser.exit(1, "Passwords do not match.\n")
    if len(password.encode("utf-8")) > 72:
        parser.exit(1, "Use a password of up to 72 UTF-8 bytes.\n")
    try:
        account = UserCreate(email=args.email, name=args.name, password=password)
    except ValidationError as error:
        for issue in error.errors(include_input=False):
            print(f"{issue['loc'][0]}: {issue['msg']}")
        return 1

    first_name, _, last_name = account.name.partition(" ")
    with SessionLocal() as db:
        existing = db.scalar(select(User.id).where(func.lower(User.email) == account.email.lower()))
        if existing is not None:
            parser.exit(1, "That email already belongs to an account. Use a separate email for this administrator.\n")
        db.add(User(
            email=account.email,
            name=account.name,
            first_name=first_name,
            last_name=last_name,
            hashed_password=get_password_hash(account.password),
            role="admin",
        ))
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            parser.exit(1, "The account could not be created. Check that the email is available.\n")
    print(f"Administrator created for {account.email}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

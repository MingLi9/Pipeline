from typing import Optional
from models import User
from sqlalchemy.orm import Session


# Get user by username
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


# Get user by id
def get_user_by_id(db: Session, id: int) -> Optional[User]:
    user = db.query(User).filter(User.id == id).first()
    return user


# Update user details
def update_user(db: Session, user: User, **kwargs) -> User:
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


# Delete a user
def delete_user(db: Session, user_id: int) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()
    return user

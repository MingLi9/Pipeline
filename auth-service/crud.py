from datetime import datetime, timedelta
from typing import Optional
from models import User, Token
import bcrypt
from sqlalchemy.orm import Session
from config import Config


# Hash password
def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


# Register a new user
def create_user(db: Session, username: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get user by username
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


# Create a new token
def create_token(
    db: Session,
    access_token: str,
    user_id: int,
) -> Token:
    new_token = Token(
        token=access_token,
        user_id=user_id,
        expires_at=datetime.now() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token


# Get token by value
def get_token(db: Session, token_str: str) -> Optional[Token]:
    return db.query(Token).filter(Token.token == token_str).first()


# Revoke token
def revoke_token(db: Session, token: Token):
    token.revoked = True
    db.commit()
    db.refresh(token)
    return token

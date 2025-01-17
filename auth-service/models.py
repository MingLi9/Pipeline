from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    User model representing a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        password (str): Password for the user, stored as a hashed value.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        age (int): Age of the user.
        email (str): Unique email address of the user.
        tokens (list[Token]): List of tokens associated with the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    age = Column(Integer, nullable=True)
    email = Column(String(255), unique=True, nullable=True)

    tokens = relationship(
        "Token", back_populates="user", cascade="all, delete"
    )


class Token(Base):
    """
    Token model representing an authentication token for a user.

    Attributes:
        id (int): Unique identifier for the token.
        token (str): The actual token string, used for authentication.
        user_id (int): Identifier of the user associated with this token.
        issued_at (datetime): Timestamp of when the token was issued.
        expires_at (datetime): Timestamp of when the token will expire.
        revoked (bool): Indicates whether the token has been revoked.
        user (User): The user associated with this token.
    """

    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String(512), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issued_at = Column(DateTime, default=datetime.now())
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="tokens")

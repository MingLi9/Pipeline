from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    age = Column(Integer, nullable=True)
    email = Column(String(255), unique=True, nullable=True)

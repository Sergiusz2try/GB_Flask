from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from blog.config.extansions import db

from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, default=False)

    author = relationship("Author", uselist=False, back_populates="user")

    def __init__(self, username, email, password, is_staff):
        self.username = username
        self.email = email
        self.password = password
        self.is_staff = is_staff

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

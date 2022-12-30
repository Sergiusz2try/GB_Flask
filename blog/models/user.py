from sqlalchemy import Column, String, Boolean, Integer
from blog.models.database import db

from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

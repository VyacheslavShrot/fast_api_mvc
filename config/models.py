from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

metadata: MetaData = MetaData()

Base = declarative_base()

"""
            Models
"""


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))

    def __str__(self):
        return f"{self.id} {self.email} {self.password}"

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

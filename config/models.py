from sqlalchemy import Column, Integer, String, MetaData, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f"{self.id} {self.email} {self.password}"

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    text = Column(Text, nullable=False)

    user = relationship("User", back_populates="posts")

    def __str__(self):
        return f"{self.id} {self.user} {self.text[:10]}..."

    def __repr__(self):
        return f"<Post(id={self.id}, user={self.user}), text={self.text})>"

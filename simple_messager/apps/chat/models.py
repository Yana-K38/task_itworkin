from sqlalchemy import Column, Integer, String
from simple_messager.api.users.db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)

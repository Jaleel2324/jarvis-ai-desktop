from sqlalchemy import Column, Integer, String, Text
from database import Base

class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    content = Column(Text)
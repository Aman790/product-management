from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Product(Base):

    __tablename__= "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    manufacturer_info = Column(String, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    category = Column(String, index=True)

class User(Base):

    __tablename__= "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String, index=True)
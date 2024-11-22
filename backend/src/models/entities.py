from sqlalchemy import Column, Integer, String, TIMESTAMP, func, JSON, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.infra.sqlite.sqlite import Base


class CollectionEntity(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    key = Column(String(255), unique=True)
    secret = Column(String(255), nullable=False)
    exposed = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    specs = relationship('SpecEntity', back_populates="collection", cascade="all, delete")


class SpecEntity(Base):
    __tablename__ = "specs"

    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"), nullable=False)
    spec = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    collection = relationship('CollectionEntity', back_populates="specs")

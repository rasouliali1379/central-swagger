from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, JSON, func
from sqlalchemy.orm import relationship

from src.infra.sqlite.sqlite import Base


class OpenAPIVersion(Base):
    __tablename__ = "specs"

    version_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False)
    version = Column(String(50), nullable=False)
    specification = Column(JSON, nullable=False)
    change_log = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    service = relationship("Service", back_populates="openapi_versions")

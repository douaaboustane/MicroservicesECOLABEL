from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class ProductMetadata(Base):
    __tablename__ = "product_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    gtin = Column(String(14), index=True, nullable=True)
    product_name = Column(String(500), nullable=False)
    ingredients_raw = Column(Text, nullable=True)
    packaging_info = Column(Text, nullable=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=False)
    ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)
    raw_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


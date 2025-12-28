from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ParseResponse(BaseModel):
    product_id: int
    gtin: Optional[str] = None
    product_name: str
    ingredients_raw: str
    packaging_info: Optional[str] = None
    metadata: Dict[str, Any]
    

class BatchParseResponse(BaseModel):
    status: str
    total_files: int
    successful: int
    failed: int
    products: list[ParseResponse]
    

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime


class ParseRequest(BaseModel):
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    auto_extract: bool = True


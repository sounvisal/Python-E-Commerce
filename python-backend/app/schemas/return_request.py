from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ReturnRequestBase(BaseModel):
    order_number: str
    product_name: str
    product_image: Optional[str] = "/images/prod-sk2.jpg"
    product_variant: Optional[str] = "230ml"
    price: Optional[float] = 125.0
    quantity: Optional[int] = 1
    reason: str
    resolution: str
    description: Optional[str] = None
    photos: Optional[List[str]] = None

class ReturnRequestCreate(ReturnRequestBase):
    order_item_id: int
    quantity: int = Field(default=1, ge=1)
    customer_name: Optional[str] = "Sreynich Chan"
    customer_email: Optional[str] = "sreynich.chan@example.com"

class ReturnRequestUpdateStatus(BaseModel):
    refund_reference: Optional[str] = Field(default=None, min_length=3, max_length=150)
    status: str
    current_step: Optional[int] = None
    timeline: Optional[List[Dict[str, Any]]] = None

class ReturnRequestResponse(ReturnRequestBase):
    success: bool = True
    refund_reference: Optional[str] = None
    order_item_id: Optional[int] = None
    id: int
    request_number: str
    customer_name: str
    customer_email: str
    status: str
    current_step: int
    submitted_date: str
    timeline: Optional[List[Dict[str, Any]]] = None
    return_address: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReturnRequestListResponse(BaseModel):
    success: bool = True
    total: int
    data: List[ReturnRequestResponse]

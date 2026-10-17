from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: int = 1

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: str
    shipping_city: str
    shipping_postal_code: Optional[str] = None
    payment_method: Optional[str] = "card"
    discount_code: Optional[str] = None
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    product_id: Optional[int] = None
    product_name: str
    image_url: Optional[str] = None
    price: float
    quantity: int
    total: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: str
    shipping_city: str
    shipping_postal_code: Optional[str] = None
    subtotal: float
    discount: float
    shipping_fee: float
    total: float
    status: str
    payment_method: str
    created_at: Optional[datetime] = None
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = "Order processed successfully"
    data: OrderOut

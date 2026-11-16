from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from datetime import datetime, timezone

class OrderItemCreate(BaseModel):
    product_id: int
    product_name: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: int = Field(default=1, ge=1, le=999)

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: str
    shipping_city: str
    shipping_postal_code: Optional[str] = None
    payment_method: Optional[str] = "card"
    discount_code: Optional[str] = None
    checkout_key: Optional[str] = Field(default=None, min_length=20, max_length=64)
    expected_total: Optional[float] = Field(default=None, ge=0)
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
    user_id: Optional[int] = None
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
    payment_status: Optional[str] = "Paid"
    transaction_ref: Optional[str] = None
    access_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    events: list = []
    created_at: Optional[datetime] = None
    items: List[OrderItemOut] = []

    @field_serializer('created_at', 'expires_at', 'delivered_at')
    def serialize_utc(self, value):
        if value is None:
            return None
        return (value if value.tzinfo else value.replace(tzinfo=timezone.utc)).isoformat()

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = "Order processed successfully"
    data: OrderOut

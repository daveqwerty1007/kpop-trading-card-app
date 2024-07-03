from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    address: Optional[str]
    phone_number: Optional[str]

class CardSchema(BaseModel):
    id: Optional[int]
    card_name: str
    artist: str
    group: str
    album: Optional[str]
    price: float
    description: Optional[str]
    image_url: Optional[str]

class OrderSchema(BaseModel):
    id: Optional[int]
    user_id: int
    order_date: datetime
    total_amount: float

class PaymentSchema(BaseModel):
    id: Optional[int]
    order_id: int
    payment_date: datetime
    payment_method: str
    payment_status: str

class InventorySchema(BaseModel):
    id: Optional[int]
    card_id: int
    quantity_available: int

class AdminSchema(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str


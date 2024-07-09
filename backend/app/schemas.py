from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj)

    def dict(self):
        return self.model_dump()

class CardSchema(BaseModel):
    id: int
    card_name: str
    artist: str
    group: str
    album: str
    price: float
    description: str
    image_url: str

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_amount: float

    class Config:
        from_attributes = True

class PaymentSchema(BaseModel):
    id: int
    order_id: int
    payment_date: datetime
    payment_method: str
    payment_status: str

    class Config:
        from_attributes = True

class InventorySchema(BaseModel):
    id: int
    card_id: int
    quantity_available: int

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj)

    def dict(self):
        return self.model_dump()

class AdminSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True

class CartItemBase(BaseModel):
    user_id: int
    card_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class OrderItemBase(BaseModel):
    order_id: int
    card_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

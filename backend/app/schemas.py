from pydantic import BaseModel, Field, conint
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    id: int
    name: str
    email: str


    class Config:
        orm_mode = True
class UserRegisterSchema(BaseModel):

    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
class CardSchema(BaseModel):
    id: int
    card_name: str
    artist: str
    group: str
    album: Optional[str] = None
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True
class CardSchemaAdd(BaseModel):

    card_name: str
    artist: str
    group: str
    album: Optional[str] = None
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True
class OrderSchema(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_amount: float
    status: Optional[str] = None

    class Config:
        orm_mode = True

class PaymentSchema(BaseModel):
    id: int
    order_id: int
    payment_date: datetime
    payment_method: str
    payment_status: str

    class Config:
        orm_mode = True

class PaymentCreateSchema(BaseModel):
    order_id: int
    payment_date: datetime
    payment_method: str
    payment_status: str

    class Config:
        orm_mode = True

class PaymentUpdateSchema(BaseModel):
    order_id: Optional[int] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None

class InventorySchema(BaseModel):
    id: int
    card_id: int
    quantity_available: int

    class Config:
        orm_mode = True

class SettingsSchema(BaseModel):
    emailMarketing: bool

class CartItemBase(BaseModel):
    user_id: int
    card_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemAddSchema(BaseModel):
    card_id: int
    quantity: conint(gt=0) = 1

class CartItemQuantitySchema(BaseModel):
    quantity: conint(gt=0)

class CartItemSchema(CartItemBase):
    id: int

    class Config:
        orm_mode = True

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

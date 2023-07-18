from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    id: int
    name: str = Field(..., max_length=32)
    surname: str = Field(..., max_length=32)
    email: EmailStr = Field(..., description='Email field')
    password: str = Field(..., max_length=32, description='Password field')


class User(BaseModel):
    name: str = Field(..., max_length=32)
    surname: str = Field(..., max_length=32)
    email: EmailStr = Field(..., description='Email field')
    password: str = Field(..., max_length=32, description='Password field')


class OrderModel(BaseModel):
    id: int
    # id_user: int
    # id_product: int
    date_: datetime
    status: str = Field(max_length=32)


class Order(BaseModel):
    # id_user: int
    # id_product: int
    date_: datetime
    status: str = Field(max_length=32)


class ProductModel(BaseModel):
    id: int
    name: str = Field(..., max_length=32)
    description: str = Field(..., max_length=128)
    price: float = Field(..., gt=0)


class Product(BaseModel):
    name: str = Field(..., max_length=32)
    description: str = Field(..., max_length=128)
    price: float = Field(..., gt=0)

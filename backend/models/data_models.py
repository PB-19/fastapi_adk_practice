from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List

class User(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Hashed password")

class Product(BaseModel):
    product_id: int = Field(..., description="Unique product identifier")
    product_name: str = Field(..., description="Name of product")
    category: str = Field(..., description="Product category")
    unit_price: float = Field(..., description="Price per unit")
    supplier_id: int = Field(..., description="Associated supplier ID")

class Supplier(BaseModel):
    supplier_id: int = Field(..., description="Unique supplier identifier")
    supplier_name: str = Field(..., description="Name of supplier")
    location: str = Field(..., description="Supplier location")
    contact_email: EmailStr = Field(..., description="Contact email address")
    reliability_score: float = Field(..., description="Supplier reliability rating")

class Inventory(BaseModel):
    product_id: int = Field(..., description="Product identifier")
    quantity: int = Field(..., description="Available stock quantity")
    last_updated: datetime = Field(..., description="Last update timestamp")

class OrderDetail(BaseModel):
    product_id: int = Field(..., description="Ordered product ID")
    supplier_id: int = Field(..., description="Supplier ID")
    quantity: int = Field(..., description="Order quantity")
    unit_price: float = Field(..., description="Price per unit")
    subtotal: float = Field(..., description="Line item total")

class Order(BaseModel):
    order_id: int = Field(..., description="Unique order identifier")
    order_details: List[OrderDetail] = Field(..., description="List of order items")
    total_amount: float = Field(..., description="Total order amount")
    timestamp: datetime = Field(..., description="Order creation time")

class SaleDetail(BaseModel):
    product_id: int = Field(..., description="Sold product ID")
    supplier_id: int = Field(..., description="Supplier ID")
    quantity: int = Field(..., description="Sale quantity")
    unit_price: float = Field(..., description="Price per unit")
    subtotal: float = Field(..., description="Line item total")

class Sale(BaseModel):
    sale_id: int = Field(..., description="Unique sale identifier")
    sale_details: List[SaleDetail] = Field(..., description="List of sale items")
    total_amount: float = Field(..., description="Total sale amount")
    timestamp: datetime = Field(..., description="Sale creation time")
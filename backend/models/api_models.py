from pydantic import BaseModel, EmailStr
from typing import List, Dict
from backend.models.data_models import Product, Supplier

class GetProductsResponse(BaseModel):
    count: int
    products: List[Product]

    class Config:
        from_attributes = True

class CreateProductRequest(BaseModel):
    product_name: str
    category: str
    unit_price: float
    supplier_id: int

class UpdateProductRequest(BaseModel):
    product_id: int
    product_name: str
    category: str
    unit_price: float
    supplier_id: int

class GetSuppliersResponse(BaseModel):
    count: int
    suppliers: List[Supplier]

    class Config:
        from_attributes = True

class CreateSupplierRequest(BaseModel):
    supplier_name: str
    location: str
    contact_email: EmailStr
    reliability_score: float

class UpdateSupplierRequest(BaseModel):
    product_id: int
    supplier_name: str
    location: str
    contact_email: EmailStr
    reliability_score: float

class CreateOrderRequest(BaseModel):
    order_items: List[Dict]

class CreateSaleRequest(BaseModel):
    sale_items: List[Dict]
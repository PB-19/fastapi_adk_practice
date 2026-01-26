from pydantic import BaseModel
from typing import List
from backend.models.data_models import Product

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

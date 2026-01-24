from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from backend.utils import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords


class Supplier(Base):
    __tablename__ = "suppliers"
    
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_name = Column(String(200), nullable=False)
    location = Column(String(200))
    contact_email = Column(String(100))
    reliability_score = Column(Float)


class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100))
    unit_price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"))


class Inventory(Base):
    __tablename__ = "inventory"
    
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_details = Column(JSON, nullable=False)  # Stores array of order items
    total_amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())


class Sale(Base):
    __tablename__ = "sales"
    
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_details = Column(JSON, nullable=False)  # Stores array of sale items
    total_amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
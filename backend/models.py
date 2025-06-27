# backend/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(SQLModel):
    name: str
    group: str  # e.g., "Dairy", "Meat", "Vegetable"
    truck_id: str  # ID of the truck this product is on

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SensorData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str = Field(foreign_key="product.id")  # or could be truck_id + product_id
    truck_id: str
    temperature: float
    humidity: float
    shock: int
    risk_prediction: Optional[int] = Field(default=None)  # 0: Safe, 1: At Risk, 2: Spoiled
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PredictionResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    risk_level: int  # 0: Safe, 1: At Risk, 2: Spoiled
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    timestamp: datetime

class SensorDataCreate(SQLModel):
    product_id: str
    truck_id: str
    temperature: float
    humidity: float
    shock: int

class SensorDataRead(SensorDataCreate):
    id: int
    risk_prediction: Optional[int]
    timestamp: datetime
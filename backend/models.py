from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    temperature: float
    humidity: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

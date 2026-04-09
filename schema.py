
from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    category: CategoryRead
    class Config:
        orm_mode = True

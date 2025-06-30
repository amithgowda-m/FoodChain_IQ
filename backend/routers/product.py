from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Product
from database import get_session

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/")
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@router.post("/")
def add_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

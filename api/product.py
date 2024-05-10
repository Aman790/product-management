import uvicorn

from fastapi import FastAPI, HTTPException, Depends, Response, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .schemas import CreateProduct, UpdateProduct, CreateUser
from .models import Product
from .database import engine, SessionLocal, get_db
from .auth import get_current_user



router = APIRouter(prefix='/product', tags=['product'])


@router.post('/product', status_code=201)
def create_product(product:CreateProduct, db:Session=Depends(get_db), user=Depends(get_current_user)):
    if user:
        db_product=Product(name=product.name, description=product.description, manufacturer_info=product.manufacturer_info, category=product.category)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    return {"message": "user not found"}

@router.get('/product/{name}', status_code=200)
def get_product_by_name(name:str, db:Session=Depends(get_db), offset: int=0, limit: int=10):
    db_result = db.query(Product).filter(Product.name==name).offset(offset).limit(limit).first()
    if not db_result:
        raise HTTPException(status_code=400, detail="category not found")
    db.commit()
    db.refresh(db_result)
    return db_result

@router.put('/product/{product_id}}', status_code=200)
def update_category(product:UpdateProduct, productr_id:int, db:Session=Depends(get_db)):
    db_result = db.query(Product).filter(Product.id == productr_id).first()
    if not db_result:
        raise HTTPException(status_code=400, detail="category not found") 
    db_result.description = product.description
    db.commit()
    db.refresh(db_result)
    return db_result



@router.delete('/product/{product_id}')
def delete_category(product_id:int, db:Session=Depends(get_db)):
    db_result = db.query(Product).filter(Product.id == product_id).first()
    if not db_result:
        raise HTTPException(status_code=400, detail="product not found") 
    db.delete(db_result)
    db.commit()
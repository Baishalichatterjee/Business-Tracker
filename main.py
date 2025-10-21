from fastapi import Depends,FastAPI,HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



database_models.Base.metadata.create_all(bind=engine)
# @app.get("/")
# def greet():
#     return {"message": "Hi, I am a new learner in FastAPI."}

# Correct way to create Product objects
products = [
    Product(id=1, name="Phone", description="Budget phone", price=99.99, quantity=10),
    Product(id=2, name="Laptop", description="Gaming laptop", price=999.00, quantity=6),
    Product(id=6, name="smart wtach", description="A smart watch", price=9999.99, quantity=1),
    Product(id=3, name="perfume", description="A beautiful smell", price=200.00, quantity=16),
]
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    db=session()
    count=db.query(database_models.Product).count

    if count == 0 :
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        
    
    db.commit()


init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all() 
    return db_products


@app.get("/products/{id}")
def get_prodcut_by_id(id:int , db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product :
        return db_product
    return "Product not found"


@app.post("/products")
def add_product(product:Product,db:Session = Depends(get_db)):  
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return products


@app.put("/products/{id}", response_model=None, status_code=status.HTTP_200_OK)
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # update fields
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)   # refresh optional but useful
    return {"message": "Updated Successfully", "product": {
        "id": db_product.id,
        "name": db_product.name,
        "description": db_product.description,
        "price": db_product.price,
        "quantity": db_product.quantity
    }}

@app.delete("/products/{id}", status_code=status.HTTP_200_OK)
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Deleted Successfully", "id": id}
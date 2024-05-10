import uvicorn


from fastapi import FastAPI
from api.database import engine, Base
from api import product, auth


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"World"}


app.include_router(product.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
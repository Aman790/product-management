from pydantic import BaseModel


class CreateProduct(BaseModel):
    id: int
    name: str
    manufacturer_info: str
    category: str
    description: str


class UpdateProduct(BaseModel):
    description: str

class DeleteProduct(BaseModel):
    name: str

class CreateUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
#Python
from typing import Optional

from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body

app = FastAPI()

# Models

class Person(BaseModel):
    first_name : str
    last_name : str
    age: Optional[int] = None
    hair_color:Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

# request and response body

@app.post("/person/new")
def create_user(person:Person = Body(...)):
    return person
    
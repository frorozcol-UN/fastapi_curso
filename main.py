#Python
from email.policy import default
from typing import Optional

from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body, Path, Query

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

# Validaciones: Query Parametros
@app.get("/person/detail")
def show_person(
    name : Optional[str]= Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Personal Name",
        description="This is the person name. It's between1 and 50 cha"),
    age  : str = Query(
        ...,
        title="Age",
        description="This is the person age, It's required"
        )
    ):
    return {name:age}


# Validation Path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id:int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the ID of the person"
    )
    ):
    return {person_id:"It exists"}

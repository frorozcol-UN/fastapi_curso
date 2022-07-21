#Python
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, HttpUrl

#FastAPI
from fastapi import FastAPI, Body, Path, Query

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Person(BaseModel):
    first_name : str = Field(
        ..., 
        min_length=1,
        max_length=50,

        )
    last_name : str = Field(
        ..., 
        min_length=1,
        max_length=50,
        
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        )
    email : EmailStr = Field(
        ...,
        title='Email',
        description='The email of the person that will receive the package.'
         )
    url : HttpUrl = Field(
        ...,
        title="Website",
        description="This is a url from website"
    )
    hair_color:Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Location(BaseModel):
    city: str = Field(
        ..., 
        min_length=5,
        max_length=20,

        )
    state:str = Field(
        ...,
        min_length=5,
        max_length=20,
    )
    country: str = Field(
        ...,
        min_length=5,
        max_length=20,
    )

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


# Validaciones. Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description="This is person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
    ):
    results = person.dict()
    results.update(location.dict())
    return results


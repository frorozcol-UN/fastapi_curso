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
        example="Alberto"

        )
    last_name : str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="ORozco"
        
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=23
        )
    email : EmailStr = Field(
        ...,
        title='Email',
        description='The email of the person that will receive the package.',
        example="freorozcoloa@gmail.com"
         )
    url : HttpUrl = Field(
        ...,
        title="Website",
        description="This is a url from website",
        example="fredy.com"
    )
    hair_color:Optional[HairColor] = Field(default=None,example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)

    """
    class Config:
        schema_extra = {
            "example":{

                "first_name": "Fredy",
                "last_name": "Orozco Loaiza",
                "age": 21,
                "email": "fredy@example.com",
                "url": "www.fredy.com",
                "hair_color": HairColor.blonde,
                "is_married":False
            }
        }
        """
    password: str = Field(
        ..., 
        min_length=8
        )


class Location(BaseModel):
    city: str = Field(
        ..., 
        min_length=5,
        max_length=20,
        example="MEdellin"

        )
    state:str = Field(
        ...,
        min_length=5,
        max_length=20,
        example="Antioquia"
    )
    country: str = Field(
        ...,
        min_length=5,
        max_length=20,
        example="Colombia"
    )


@app.get("/")
def home():
    return {"Hello": "World"}

# request and response body

@app.post("/person/new", response_model=Person, response_model_exclude={"password"})
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
        description="This is the person name. It's between1 and 50 cha",
        example="Fredy"
        ),
    age  : str = Query(
        ...,
        title="Age",
        description="This is the person age, It's required",
        example=23
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
        description="This is the ID of the person",
        example=123
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
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
    ):
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person


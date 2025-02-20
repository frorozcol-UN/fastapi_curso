#Python
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, HttpUrl

#FastAPI
from fastapi import (
    Cookie, 
    FastAPI, 
    Body, 
    File, 
    Header, 
    Path, 
    Query, 
    UploadFile, 
    status, 
    Form,
    HTTPException
)
app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class PersonBase(BaseModel):
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
        example="https://platzi.com/clases/2514-fastapi-modularizacion-datos/41981-status-code-personalizados/"
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

class Person(PersonBase):
     password: str = Field(
        ..., 
        min_length=8
        )

class PersonOut(PersonBase):
    pass

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

class Login(BaseModel):
    username:str = Field(
        ...,
        max_length=20,
        example="Freorozcoloa"
    )
    message: str = Field(default="Login Succesfully!")

    
@app.get(
    "/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

# request and response body

@app.post(
    "/person/new", 
    response_model=Person, 
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Creates Person in the app."
    )
def create_user(person:Person = Body(...)):
    """Create Person

    This path operation, create a person in the app and save information in the database

    Args:
        -Request body parameter:
        -**person: Person** -> A Person model with first name, last name, age and is_married

    Returns:
        -Person model with first name, last name, age, hair color and marital staus.
    """    
    return person

# Validaciones: Query Parametros
@app.get(
    "/person/detail",
    status_code=status.HTTP_200_OK,
    deprecated = True
    )
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
        ),
    tags=["Persons"],
    
    ):
    return {name:age}

persons = {1, 2, 3, 4, 5}
# Validation Path parameters
@app.get(
    "/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"])
def show_person(
    person_id:int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the ID of the person",
        example=123
    )
    ):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="!This person dosen't exists!"
        )
    return {person_id:"It exists"}


# Validaciones. Request Body
@app.put(
    "/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"]
    )
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

@app.post(
    path="/login",
    response_model=Login,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def loggin(username:str = Form(...), password:str = Form(...) ):
    return Login(username=username)

# Cookies and Headers Parameters.

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example="Fredy"
        ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example="Orozco"
        ),
    email: EmailStr = Form(
        ...,
        example="freorozcoloa@example.com"
        ),
    message: str = Form(
        ...,
        min_length=20,
        example="Querido fredy espero que este bien, todo bien todo bonito"
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)

):
    return user_agent


#Files

@app.post(
    path="/post-img"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(Kb)":round(len(image.file.read())/1024 ,2),
    }
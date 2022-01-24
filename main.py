#Python - Respetar el orden es super importante, que va primero y que va despues.
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    yellow = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Camilin"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Duarte"
    )
    age: int = Field(
        ...,
        gt=0,
        le=200,
        example = "25"
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(..., min_length = 8)
    #class Config:
    #    schema_extra = {
    #        "example": {
    #            "first_name": "Camilo",
    #            "last_name": "Duarte",
    #            "age": 25,
    #            "hair_color": "black",
    #            "is_married": False
    #        }
    #    }

class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Camilin"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Duarte"
    )
    age: int = Field(
        ...,
        gt=0,
        le=200,
        example = "25"
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    #class Config:
    #    schema_extra = {
    #        "example": {
    #            "first_name": "Camilo",
    #            "last_name": "Duarte",
    #            "age": 25,
    #            "hair_color": "black",
    #            "is_married": False
    #        }
    #    }
@app.get("/")
def home():
    return {"Hello": "World"}

#Resquest and response body

@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person

#validaciones: Query parameters

@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(
            None, min_length=1,
            max_length=50,
            title= "Person Name",
            description= "This is the person name. It's between 1 and 50 characters",
            example= "Rocio"
        ),
        age: str = Query(
            ...,
            title="Person Age",
            descriptrion="This is the person Age, It is required",
            example= 25
        )
):
    return{name: age}

#Validaciones path parameters

@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(..., gt=0, example=123)
):
    return  {person_id: "It exist!"}

#validaciones: Request body
@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person ID",
            description= "This is the person ID",
            gt=0,
            example=25
        ),
        person: Person = Body(...),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
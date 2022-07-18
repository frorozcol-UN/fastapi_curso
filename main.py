from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}

# request and response body

@app.post("/person/new")
def create_user():
    pass
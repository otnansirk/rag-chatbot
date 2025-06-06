from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI
from services.knowlage import Knowlage
load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/v1/query")
def search(q: Union[str, None] = None):
    knowlage = Knowlage()
    if q == None: 
        return {
            "message": "Please write the query"
        }
    
    res = knowlage.query(q)
    return res


from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI
from services.knowlage import Knowlage
from helpers import responses
from models.knowlage import KnowlageSearchModel


load_dotenv()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/v1/query")
def search(body: KnowlageSearchModel):
    knowlage = Knowlage(body.company)
    try:
        res = knowlage.query(body.q)
        return responses.success(res)
    except Exception as e:
        return responses.error(str(e))


@app.post("/v1/upload")
def search(q: Union[str, None] = None):
    knowlage = Knowlage()
    if q == None: 
        return {
            "message": "Please write the query"
        }
    
    res = knowlage.query(q)
    return res


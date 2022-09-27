import requests
from fastapi import FastAPI
from Ex2_CesarCypher import cypher, decypher
from random import randint
from pydantic import BaseModel
import uvicorn

app = FastAPI()


def get_fact():
    response = requests.get('https://dog-api.kinduff.com/api/facts')
    return response.json()['facts'][0]

class Fact(BaseModel):
    crypted: str
    key: int

@app.get("/getCifra")
def get_cifra():
    fact = get_fact()
    key = randint(1, 25)
    cyphered = cypher(fact, key)
    return {'crypted': cyphered, 'key': key}

@app.post("/resolveCifra")
def resolve_cifra(fact: Fact):
    cyphered, key = fact
    decrypted = decypher(cyphered[1], key[1])
    return {'decrypted': decrypted}

if __name__ == "__main__":
    uvicorn.run("Ex3_DogsCypher:app", port=5000, log_level="info")
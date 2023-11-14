import random
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel

class Number(BaseModel):
    number: str

app = FastAPI()

@app.post('/api/')
async def check(number: Number):
    r = random.randint(0, 5)
    await asyncio.sleep(r)
    return {"result": random.choice([True, False])}
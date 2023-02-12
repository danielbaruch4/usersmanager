from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from functools import wraps

import time
import asyncio

def timeit(func):
    @wraps(func)
    async def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
@timeit
async def read_root():
    return {"Hello": "World"}

counter = 0
@app.post("/login")
async def login(username):
    counter+=1 
    return {"success":True,"user_id":counter,'username':username}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# running the app from cmd
# python -m uvicorn main:app --reload

if __name__ == "__main__":
    uvicorn.run('server:app',port=5000,host="127.0.0.1",reload=True)


# if __name__ == "__main__":
#     uvicorn.run('server:app',port=5000,host="0.0.0.0",reload=True)



# from flask import Flask
# print("flask server")


# app = Flask(__name__)
# print(__name__)

# @app.route('/')
# def test():
#     return {'data':[1,2,3]}

# @app.route('/hello')
# def hello():
#     return 'Hello, World!'
    
# if __name__ == '__main__':
#   app.run(host='0.0.0.0', debug=False)
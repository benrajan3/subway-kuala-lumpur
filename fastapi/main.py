"""
Testing FastAPI
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/subway-data/all")   # function below is handling get request
# async used in case of multiple input or output operations
async def read_all_data():
    return {"message": "Hello World"}
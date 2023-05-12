from fastapi import FastAPI, Query


description = """
FastPokeAPI helps you find pokemon through their single type or dual types. 🚀

The endpoints are below and using a curl request, or using Insomnia.

You can apply post requests and obtain the data you need and the data will be recieved as a JSON filled with Pokemon data.

Hopefully all of the documentation provided is explained clearly and the endpoints themselves provide the correct data.

Thank you for reading this portion of the documentation.
"""

app = FastAPI(
    title="FastPokeAPI",
    description=description,
    version="0.0.1",
)

# Defining a route for the root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

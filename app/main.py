# Loading the needed libraries
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List
from app.poke_query_duck import (
    get_pokemon_by_single_type, 
    get_pokemon_by_dual_type
)

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

class PokemonData(BaseModel):
    name: str                    # Not Null
    url: str                     # Not Null
    type_1: str                  # Not Null
    type_2: Optional[str] = None # Can be Null



# Defining a route for the root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Defining the end point where a single type is requested as well as requesting an exact type
@app.post("/pokemon_single_type/{pokemon_type}")
async def pokemon_single_type(pokemon_type: str, exact: bool = Query(False)) -> List[PokemonData]:
    """
    Retrives a Array of JSON Pokemon data that match the given type and specifying if you want exactly that type.

    Args:
        
        pokemon_type (str): The name of the type to search for.

        exact (bool): 
                      If True, only return Pokemon that have the specified type as their sole type. 
                      
                      If False, return Pokemon that have the specified type as one of their types.

    Returns:
        
        Array of JSON: A list of Pokemon matching the given type, represented as a json to the end user.
    """
    pokemon_list = get_pokemon_by_single_type(pokemon_type, exact)
    return pokemon_list


# Defining the endpoint when two types are requested
@app.post("/pokemon_dual_type/{pokemon_types}")
async def pokemon_dual_type(pokemon_types: str) -> List[PokemonData]:
    """
    Retrieves Array of JSON of Pokemon that match the given two types.

    Args:
        
        pokemon_types (str): A string representing the dual type, formatted as "type_1-type_2". 
                      If only one type is specified,"type_1", the function will search for Pokemon with that single type and other types.

    Returns:
        
        Array of JSON: A list of Pokemon matching the given type(s), represented as json to the end user.
    """
    if "-" in pokemon_types:
        pokemon_list = get_pokemon_by_dual_type(pokemon_types)
        return pokemon_list
    else:
        return []
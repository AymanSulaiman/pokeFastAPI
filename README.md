# fastpokeapi-ayman

## Tools and technologies
Diagrams package, using images
* Polars - Data Manipluation
* DuckDB - static in-memory version of SQLite, can load csv and parquet files
* FastAPI - Backend
* Mage.ai - Orchestration
* Streamlit - Frontend
* Matplotlib - Radar Graphs
* Docker Compose

## How to Run
Run the following commmand given that you have docker installed

````bash
docker-compose up --build
````

## What should spin up
* FastAPI - `localhost:8000` 
* Mage.AI - `localhost:6789`
* Streamlit - `localhost:8501`

## Data file format
* The pokemon pokemon are stored in a parquet file as a parquet file uses efficient data compression and encoding scheme for fast data storing and retrieval. With DuckDB, we can load the data via it's own SQL accent/dialect and query the data directly whilst it's in memory.

## How the data was initally collected and exported
```python
import polars as pl
import httpx
import numpy as np
import os

URL = "https://pokeapi.co/api/v2/pokemon/?limit="

def retrieve_first_gen(url: str):
    """
    Retrieves the Pokemon data from the PokeAPI and returns it as a Polars DataFrame.

    Args:
    - url: A string representing the URL of the PokeAPI endpoint to retrieve data from.

    Returns:
    - A Polars DataFrame containing the Pokemon data.
    """
    first_gen = httpx.get(url).json()
    first_gen_df = pl.DataFrame(first_gen['results'])
    return first_gen_df

def extend_pokemon_types(pokemon_df):
    """
    Extends the given Polars DataFrame `pokemon_df` by adding two columns, "type_1" and "type_2", containing the 
    primary and secondary types of each Pokemon, respectively. The types are obtained by sending an HTTP GET request 
    to the URL of each Pokemon in the "url" column of the DataFrame, and parsing the JSON response. If a Pokemon has 
    only one type, its "type_2" value is set to NaN.

    Args:
    - pokemon_df: A Polars DataFrame containing a "url" column with URLs of Pokemon to extend with types.

    Returns:
    - A new Polars DataFrame with the same columns as `pokemon_df`, plus the "type_1" and "type_2" columns.
    """
    pokemon_list = pokemon_df["url"].to_list()
    type_1, type_2 = [], []
    for pokemon_url in pokemon_list:
        pokemon_json = httpx.get(pokemon_url).json()
        types = pokemon_json['types']
        if len(types) == 1:
            type_1.append(types[0]['type']['name'])
            type_2.append(np.nan)
        elif len(types) == 2:
            type_1.append(types[0]['type']['name'])
            type_2.append(types[1]['type']['name'])
        else:
            type_1.append(np.nan)
            type_2.append(np.nan)

    first_gen_df = pokemon_df.with_columns([
        pl.Series(name="type_1", values=type_1),
        pl.Series(name="type_2", values=type_2)
    ])
    return first_gen_df

def main():
    """
    Retrieves the first generation of Pokemon data from the PokeAPI, extends it with type information using 
    `extend_pokemon_types()`, and writes the resulting DataFrame to a Parquet file.

    Args:
    - None

    Returns:
    - None
    """
    first_gen_df = retrieve_first_gen(URL+"1015")
    pokemon_df = extend_pokemon_types(first_gen_df)
    pokemon_df.write_parquet(os.path.join('..','data','pokemon_from_mage.parquet'))

if __name__ == '__main__':
    print("Starting collecting pokemon data")
    main()
    print("Finished!")
```

How the PokeData loaded locally.
```python
# Importing DuckDB
import duckdb

# Connecting to the 'pokemon_from_mage.parquet' table
db = duckdb.sql("""
    SELECT
        *
    FROM
        'data/pokemon_from_mage.parquet'
""")
```

## The paths and the python functions

Post Request and python code of a pokemon single type

Curl Request
```bash
localhost:8000/pokemon_single_type/{pokemon_type}?exact=true
curl -X 'POST' \
  'http://localhost:8000/pokemon_single_type/grass?exact=false' \
  -H 'accept: application/json' \
  -d ''
```

Python Function
```python
def get_pokemon_by_single_type(pokemon_type, exact):
    """
    retrives a list of Pokemon dicts that match the given type.

    Args:
        pokemon_type (str): The name of the type to search for.
        exact (bool): If True, only return Pokemon that have the specified type as their sole type. 
                      If False, return Pokemon that have the specified type as one of their types.

    Returns:
        list of dicts: A list of Pokemon matching the given type, represented as a json to the end user.
    """
    if exact:
        # Filtering the database to get pokemon with specific type as their sole type.
        data = db.filter(f"""
        (
            lower(type_1) = lower('{pokemon_type}') AND type_2 IS NULL
        ) 
        OR 
        (
            lower(type_2) = lower('{pokemon_type}') AND type_1 IS NULL
        )
        """)
    else:
        # Filtering the database to get pokemon with specific type.
        data = db.filter(f"""
        lower(type_1) = lower('{pokemon_type}') 
        OR 
        lower(type_2) = lower('{pokemon_type}')
        """)
        print(data)
    # Converting the data from the DuckDB result to a list of dictionaries
    # complient with the PokemonData class in the FastAPI main.py file.
    return data.to_df().to_dict(orient='records')
```

Post Request and python code of a pokemon dual type

Curl Requests
```bash
localhost:8000/pokemon_dual_type/{pokemon_types}
curl -X 'POST' \
  'http://localhost:8000/pokemon_dual_type/grass-poison' \
  -H 'accept: application/json' \
  -d ''
```
Python Function
```python
def get_pokemon_by_dual_type(string):
    """
    Get a list of Pokemon that match the given two types.

    Args:
        string (str): A string representing the dual type, formatted as "type_1-type_2". 
                      If only one type is specified,"type_1", the function will search for Pokemon with that single type and other types.

    Returns:
        Array of JSON: An array of Pokemon matching the given type(s), represented as JSON to the end user.
    """

    # Splitting the input string into two types
    txt = string.split("-") if "-" in string else [string]

    # Seperating the types to their own variables
    type_1=txt[0] 
    type_2=txt[1] if len(txt)==2 else None
    
    if type_2==None:
        
        # Filtering the database to get Pokemon with the specified type as their sole or dual type
        # This is an edge case and shouldn't be activated.
        data = db.filter(f"""
        lower(type_1) = lower('{type_1}')
        """)
    else:
        
        # Filtering the database to get Pokemon with the specified types as their dual type
        data = db.filter(f"""
        (
            lower(type_1) = lower('{type_1}') AND lower(type_2) = lower('{type_2}')
        )
        OR
        (
            lower(type_2) = lower('{type_1}') AND lower(type_1) = lower('{type_2}')
        )
        """)

    # Converting the resulting DuckDB result set to a list of dictionaries
    return data.to_df().to_dict(orient='records')

```

```bash
# FastPokeAPI Documention
localhost:8000/docs
```
## Next Phase
The next phase of the API project would be able to either implement or serve the following:
* Deploy to a cloud service provider or an on-prems system for daily use by others.
* Listen to feedback and improve the API overtime and adding functionality.
* Implement a pokedex functionality with either Streamlit or Tableau, this would require DBT (Data Build Tools) that can be used by mage.
* Transfer the data from a data lake/local to SQL so the data can be accessed by different teams.
* Incorperate security to the API with JWT.

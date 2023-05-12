# Importing DuckDB
import duckdb

# Connecting to the 'pokemon_first_gen.parquet' table
db = duckdb.sql("""
    SELECT
        *
    FROM
        'data/pokemon_from_mage.parquet'
""")


def get_pokemon_by_single_type(pokemon_type: str, exact: bool) -> list:
    """
    retrives a list of Pokemon dicts that match the given type.

    Args:
        pokemon_type (str): The name of the type to search for.
        exact (bool): If True, only return Pokemon that have the specified type as their sole type. 
                      If False, return Pokemon that have the specified type as one of their types.

    Returns:
        Array of JSON: An array of Pokemon matching the given type, represented as a JSON to the end user.
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

    # Converting the data from the DuckDB result to a list of dictionaries
    # complient with the PokemonData class in the FastAPI main.py file.
    return data.to_df().to_dict(orient='records')

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

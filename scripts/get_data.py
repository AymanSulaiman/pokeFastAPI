import polars as pl
import httpx
import numpy as np
import os

# Main pokemon api URL
URL = "https://pokeapi.co/api/v2/pokemon/?limit="

def retrieve_first_gen(url: str):
    """
    Retrieves the first generation of Pokemon data from the PokeAPI and returns it as a Polars DataFrame.

    Args:
    - url: A string representing the URL of the PokeAPI endpoint to retrieve data from.

    Returns:
    - A Polars DataFrame containing the first generation of Pokemon data.
    """

    # Makes a call to retrieve a certain number of pokemon
    first_gen = httpx.get(url).json()

    # Using Polars
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

    # Extract the list of URLs from the "url" column of the Polars DataFrame.
    pokemon_list = pokemon_df["url"].to_list()

    # Initialize empty lists to store the primary and secondary types of each Pokemon.
    type_1, type_2 = [], []

    # Loop over the list of URLs and send an HTTP GET request to each URL to obtain the types of the corresponding
    # Pokemon.
    for pokemon_url in pokemon_list:
        pokemon_json = httpx.get(pokemon_url).json()
        types = pokemon_json['types']

        # If the Pokemon has only one type, set its "type_2" value to NaN via numpy.
        if len(types) == 1:
            type_1.append(types[0]['type']['name'])
            type_2.append(np.nan)

        # If the Pokemon has two types, store its primary and secondary types in the "type_1" and "type_2" lists,
        # respectively.
        elif len(types) == 2:
            type_1.append(types[0]['type']['name'])
            type_2.append(types[1]['type']['name'])
            
        # If the Pokemon has no types (which should not happen), set both its "type_1" and "type_2" values to NaN
        # This is an edge case since every pokemon should have a primary type.
        else:
            type_1.append(np.nan)
            type_2.append(np.nan)
    # Appending new columns to the current Polars DataFrame with the primary and secondary types of each Pokemon.
    # It is faster in Polars compared to Pandas due to the Rust Backend.
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

    # Obtaining every single pokemon
    first_gen_df = retrieve_first_gen(URL+"1015")
    
    # Running the function above
    pokemon_df = extend_pokemon_types(first_gen_df)

    # Writing the parquet locally
    pokemon_df.write_parquet(os.path.join('..','data','pokemon_from_script.parquet'))

if __name__ == '__main__':
    print("Starting collecting pokemon data")
    main()
    print("Finished!")
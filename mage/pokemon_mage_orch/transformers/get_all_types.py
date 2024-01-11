import polars as pl
import numpy as np
import httpx

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


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
    
    pokemon_df = pl.from_pandas(pokemon_df)

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

        # If the Pokemon has no types (This is an edge case), set both its "type_1" and "type_2" values to NaN
        # This is an edge case since every pokemon should have a primary type.
        else:
            type_1.append(np.nan)
            type_2.append(np.nan)

    # Appending new columns to the current Polars DataFrame with the primary and secondary types of each Pokemon.
    # It is faster in Polars compared to Pandas due to the Rust Backend.
    pokemon_df = pokemon_df.with_columns([
        pl.Series(name="type_1", values=type_1),
        pl.Series(name="type_2", values=type_2)
    ])
    
    # Converting the Polars datafrom to a pandas dataframe for the data exporter
    return pokemon_df.to_pandas()


@transformer
def transform(pokemon_df, *args, **kwargs):
    """
    Template code for a transformer block.
    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.
    Args:
        args: The input variables from upstream blocks
    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    pokemon_df = extend_pokemon_types(pokemon_df)
    return pokemon_df


@test
def test_output(pokemon_df) -> None:
    """
    Template code for testing the output of the block.
    """

    print(len(pokemon_df.loc[pokemon_df["type_1"]=="fire"]))

    assert len(pokemon_df) == 1015, 'There should be exactly 151 pokemon'
    assert pokemon_df["name"][0] == "bulbasaur" # First Pokemon should be the best starter pokemon
    assert pokemon_df["name"][150] == "mew"     # Last Pokemon should be Mew, in terms of first generation
    # assert len(first_gen_types_df.loc[first_gen_types_df["type_1"]=="fire"]) == 12

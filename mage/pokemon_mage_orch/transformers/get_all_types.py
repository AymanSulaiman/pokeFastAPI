import polars as pl
import numpy as np
import httpx

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def extend_pokemon_types(pokemon_df):
    pokemon_df = pl.from_pandas(pokemon_df)
    pokemon_list = pokemon_df["url"].to_list()
    type_1, type_2 = [], []
    for pokemon_url in pokemon_list:
        pokemon_json = httpx.get(pokemon_url).json()
        # print(pokemon_json)
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

    pokemon_df = pokemon_df.with_columns([
        pl.Series(name="type_1", values=type_1),
        pl.Series(name="type_2", values=type_2)
    ])
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

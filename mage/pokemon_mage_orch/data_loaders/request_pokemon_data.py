import httpx
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

URL = "https://pokeapi.co/api/v2/pokemon/?limit="

@data_loader
def load_data():
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Makes a call to retrieve a certain number of pokemon
    pokemon = httpx.get(URL+"1015").json()
    # Using pandas to load the results into a dataframe
    pokemon_df = pd.DataFrame(pokemon['results'])
    return pokemon_df


@test
def test_output(pokemon_df) -> None:
    """
    The tests below assert the fact that this is the first gen pokemon
    Test 1 affrims that there are 1015 pokemon in the dataset
    Test 2 affirms that bulbasaur is the first pokemon in the dataframe
    Test 3 affirms that mew is the last pokemon in the dataframe 
    """
    assert len(pokemon_df) == 1015, 'There should be exactly 151 pokemon'
    assert pokemon_df["name"][0] == "bulbasaur" # First Pokemon should be the best starter pokemon
    assert pokemon_df["name"][150] == "mew"     # Last Pokemon should be Mew, in terms of first generation



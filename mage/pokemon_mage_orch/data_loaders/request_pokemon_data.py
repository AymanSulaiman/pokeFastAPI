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
    # Specify your data loading logic here
    first_gen = httpx.get(URL+"1015").json()
    first_gen_df = pd.DataFrame(first_gen['results'])
    return first_gen_df


@test
def test_output(first_gen_df) -> None:
    """
    The tests below assert the fact that this is the first gen pokemon
    Test 1 affrims that there are 1015 pokemon in the dataset
    Test 2 affirms that bulbasaur is the first pokemon in the dataframe
    Test 3 affirms that mew is the last pokemon in the dataframe 
    """
    assert len(first_gen_df) == 1015, 'There should be exactly 151 pokemon'
    assert first_gen_df["name"][0] == "bulbasaur" # First Pokemon should be the best starter pokemon
    assert first_gen_df["name"][150] == "mew"     # Last Pokemon should be Mew, in terms of first generation



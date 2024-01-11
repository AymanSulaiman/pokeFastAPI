import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import requests


POKEAPI_URL = "http://app:8000"

def get_pokemon_data(pokemon_url):
    """
    Retrieve Pokemon data from the given URL.
    """
    pokemon_json = requests.get(pokemon_url).json()
    # Extract relevant data from the JSON response
    name = pokemon_json['name']
    stats = pokemon_json['stats']
    sprites = pokemon_json['sprites']
    types = pokemon_json['types']
    return {
        "name": name, 
        "stats": stats, 
        "sprites": sprites,
        "types": types
        }

def get_pokemon_sprite(pokemon_data):
    """
    Retrieve the sprite of the Pokemon from its data.
    """
    sprite_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
    response = requests.get(sprite_url)
    return response.content if response.status_code == 200 else None


def get_pokemon_stats(pokemon_data):
    """
    Extract the types of the Pokemon from its data.
    """
    stats = pokemon_data['stats']
    stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in stats}
    return stats_dict

def get_pokemon_types(pokemon_data):
    """
    Extract the types of the Pokemon from its data.
    """
    types = pokemon_data['types']
    types_list = [typ['type']['name'] for typ in types]
    return types_list

def fetch_pokemon_dual_type(type1, type2):
    """
    Fetch Pokemon with dual types from the PokeAPI.
    """
    response = requests.post(f"{POKEAPI_URL}/pokemon_dual_type/{type1}-{type2}")
    if response.status_code == 200:
        types_data = response.json()
        dual_type_pokemon = []
        for pokemon in types_data:
            pokemon_url = pokemon['url']
            pokemon_data = get_pokemon_data(pokemon_url)
            dual_type_pokemon.append(pokemon_data)
        return dual_type_pokemon
    return None

def fetch_pokemon_single_type(pokemon_type, exact_match):
    """
    Fetch Pokemon with a single type from the PokeAPI.
    """
    response = requests.post(f"{POKEAPI_URL}/pokemon_single_type/{pokemon_type}?exact={exact_match}")
    if response.status_code == 200:
        types_data = response.json()
        single_type_pokemon = []
        for pokemon in types_data:
            pokemon_name = pokemon['url']
            pokemon_data = get_pokemon_data(pokemon_name)
            if exact_match:
                if [pokemon_type] == get_pokemon_types(pokemon_data):
                    single_type_pokemon.append(pokemon_data)
            else:
                if pokemon_type in get_pokemon_types(pokemon_data):
                    single_type_pokemon.append(pokemon_data)
        return single_type_pokemon
    return None

def create_radar_graph(pokemon_data):
    """
    Create a radar graph based on the Pokemon's stats.
    """
    pokemon_name = pokemon_data['name']
    pokemon_stats = get_pokemon_stats(pokemon_data)

    stats_df = pd.DataFrame(pokemon_stats, index=[0])
    num_stats = len(pokemon_stats)
    stat_names = list(pokemon_stats.keys())
    stat_values = list(pokemon_stats.values())
    stat_values.append(stat_values[0])
    angles = [n / float(num_stats) * 2 * pi for n in range(num_stats)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={"projection": "polar"})
    ax.fill(angles, stat_values, color="skyblue", alpha=0.7)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stat_names)
    ax.set_yticklabels([])
    ax.set_title("Stats", fontsize=12)
    ax.spines["polar"].set_visible(False)

    # Add numbers on the chart
    for angle, stat_value, stat_name in zip(angles, stat_values[:-1], stat_names):
        ax.text(angle, stat_value, str(stat_value), ha='center', va='center')

    # Set y-axis limits
    ax.set_ylim(0, max(stat_values)*1.5)

    return fig



def main():
    st.title("Pokemon Stats and Sprites")


    st.sidebar.header("Search Pokemon by Type")
    type_option = st.sidebar.radio("Select search option", ("Dual Type", "Single Type"))

    if type_option == "Dual Type":
        st.sidebar.subheader("Select Types")
        type1 = st.sidebar.selectbox("Type 1", ["normal", "fire", "water", "electric", "grass", "ice",
                                                 "fighting", "poison", "ground", "flying", "psychic",
                                                 "bug", "rock", "ghost", "dragon", "dark", "steel",
                                                 "fairy"])
        type2 = st.sidebar.selectbox("Type 2", ["normal", "fire", "water", "electric", "grass", "ice",
                                                 "fighting", "poison", "ground", "flying", "psychic",
                                                 "bug", "rock", "ghost", "dragon", "dark", "steel",
                                                 "fairy"])

        if type1 != type2:
            dual_type_pokemon = fetch_pokemon_dual_type(type1, type2)
            if dual_type_pokemon:
                st.header("Dual Type Pokemon")
                for pokemon_data in dual_type_pokemon:
                    pokemon_name = pokemon_data['name']
                    pokemon_sprite = get_pokemon_sprite(pokemon_data)
                    pokemon_stats = get_pokemon_stats(pokemon_data)

                    st.subheader(pokemon_name.capitalize())
                    st.image(pokemon_sprite, use_column_width=True)

                    st.write("Type:", ", ".join(get_pokemon_types(pokemon_data)))
                    st.write("Stats:")
                    for stat_name, stat_value in pokemon_stats.items():
                        st.write(f"{stat_name.capitalize()}: {stat_value}")
                    fig = create_radar_graph(pokemon_data)
                    st.pyplot(fig)
                    st.write("---")

            else:
                st.warning("No dual type Pokémon found for the selected types.")

        else:
            st.warning("Please select different types for Type 1 and Type 2.")

    elif type_option == "Single Type":
        st.sidebar.subheader("Select Type")
        pokemon_type = st.sidebar.selectbox("Type", ["normal", "fire", "water", "electric", "grass", "ice",
                                                     "fighting", "poison", "ground", "flying", "psychic",
                                                     "bug", "rock", "ghost", "dragon", "dark", "steel",
                                                     "fairy"])

        exact_match = st.sidebar.checkbox("Exact Match", value=False)

        single_type_pokemon = fetch_pokemon_single_type(pokemon_type, exact_match)
        if single_type_pokemon:
            st.header("Single Type Pokémon")
            for pokemon_data in single_type_pokemon:
                pokemon_name = pokemon_data['name']
                pokemon_sprite = get_pokemon_sprite(pokemon_data)
                pokemon_stats = get_pokemon_stats(pokemon_data)

                st.subheader(pokemon_name.capitalize())
                st.image(pokemon_sprite, use_column_width=True)

                st.write("Type:", ", ".join(get_pokemon_types(pokemon_data)))
                st.write("Stats:")
                for stat_name, stat_value in pokemon_stats.items():
                    st.write(f"{stat_name.capitalize()}: {stat_value}")
                fig = create_radar_graph(pokemon_data)
                st.pyplot(fig)
                st.write("---")

        else:
            st.warning("No single type Pokémon found for the selected type.")

if __name__ == "__main__":
    main()
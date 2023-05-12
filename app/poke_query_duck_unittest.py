import unittest
from poke_query_duck import get_pokemon_by_dual_type, get_pokemon_by_single_type

# Defining the test cases in a class for first gen pokemon only

class TestPokeQuerys(unittest.TestCase):

    # Test method for getting pokemon with an exact single type search query
    def test_get_pokemon_by_single_type_exact(self):
        result = get_pokemon_by_single_type('Grass', True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'],'tangela')

    # Test method for getting pokemon with an inexact single type search query
    def test_get_pokemon_by_single_type_inexact(self):
        result = get_pokemon_by_single_type('Fire', False)
        self.assertEqual(len(result), 12)
        self.assertEqual(result[0]['name'], 'charmander')
    
    # Test method for getting pokemon with a dual type search query (single type)
    def test_get_pokemon_by_dual_type_single(self):
        result = get_pokemon_by_dual_type('Grass')
        self.assertEqual(len(result), 12)
        self.assertEqual(result[0]['name'], 'bulbasaur')

    # Test method for getting pokemon with a dual type search query (dual type should work)
    def test_get_pokemon_by_dual_type_double(self):    
        result = get_pokemon_by_dual_type('Fire-Flying')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'charizard')

    # Test method for getting pokemon with a single type search query (invalid type)
    def test_get_pokemon_by_single_type_invalid(self):
        result = get_pokemon_by_single_type('InvalidType', True)
        self.assertEqual(result, [])

    # Test method for getting pokemon with a single type search query (type does not exist)
    def test_get_pokemon_by_single_type_not_exist(self):
        result = get_pokemon_by_single_type('Ghost', True)
        self.assertEqual(len(result), 0)

    # Test method for getting pokemon with a dual type search query (no pokemon found)
    def test_get_pokemon_by_dual_type_not_exist(self):
        result = get_pokemon_by_dual_type('Water-Dragon')
        self.assertEqual(len(result), 0)

    # Test method for getting pokemon with a single type search query (no pokemon found)
    def test_get_pokemon_by_single_type_no_pokemon(self):
        result = get_pokemon_by_single_type('Ice', True)
        self.assertEqual(len(result), 0)

    # Test method for getting pokemon with a dual type search query (three pokemon found)
    def test_get_pokemon_by_dual_type_no_pokemon(self):
        result = get_pokemon_by_dual_type('Water-Ice')
        self.assertEqual(len(result), 3)
    
    # Test method for getting pokemon with a single type search query (First pokemon should be Mankey)
    def test_get_pokemon_by_single_type_one_pokemon(self):
        result = get_pokemon_by_single_type('Fighting', True)
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]['name'], 'mankey')

    # Test method for getting pokemon with a dual type search query (no pokemon found until Gen 3)
    def test_get_pokemon_by_dual_type_one_pokemon(self):
        result = get_pokemon_by_dual_type('Fire-Ground')
        self.assertEqual(len(result), 0)

    # Test method for getting pokemon with a dual type search query (no pokemon found)
    def test_get_pokemon_by_dual_type_one_pokemon(self):
        result = get_pokemon_by_dual_type('FireFlying')
        self.assertEqual(len(result), 0)

    # Test method for getting pokemon with a dual type search query (Last pokemon should be Rhydon)
    def test_get_pokemon_by_dual_type_one_pokemon(self):
        result = get_pokemon_by_dual_type('Rock-Ground')
        self.assertEqual(result[-1]["name"], "rhydon")

if __name__ == '__main__':
    unittest.main()
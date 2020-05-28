import animal
from animal import Animal
import pet
from pet import Animal
from pet import Pet
from random import Random
import unittest
from unittest.mock import patch


class PetTest(unittest.TestCase):
    @patch.object(Animal, 'get_age')
    @patch.object(Animal, 'get_species')
    @patch.object(Animal, 'get_complex_object')
    def test___str__(self, mock_get_complex_object, mock_get_species, mock_get_age):
        mock_get_complex_object.return_value = Random()
        mock_get_species.return_value = 'Dog'
        mock_get_age.return_value = 12
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEqual(
            pet_instance.__str__(),
            'Random Clifford is a dog aged 13'
        )


    def test_create_pet(self):
        self.assertIsInstance(
            pet.create_pet(name='Clifford',species='Dog',age=12),
            pet.Pet
        )


    def test_get_name(self):
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEqual(
            pet_instance.get_name(),
            'Clifford'
        )


    def test_lower(self):
        self.assertEqual(
            Pet.lower(s='Dog'),
            'dog'
        )


    def test_set_age(self):
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEqual(
            pet_instance.set_age(age=13),
            None
        )


if __name__ == "__main__":
    unittest.main()

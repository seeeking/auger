from animal import Animal


class Pet(Animal):
    def __init__(self, name, species, age=0):
        Animal.__init__(self, species, age)
        self._name = name

    def get_name(self):
        return self._name

    def set_age(self, age):
        self._age = age

    @staticmethod
    def lower(s):
        return s.lower()

    def __str__(self):
        return '%s %s is a %s aged %d' % (self.get_complex_object().__class__.__name__, self.get_name(), Pet.lower(self.get_species()), self.get_age())


def create_pet(name, species, age=0):
    return Pet(name, species, age)


if __name__ == '__main__':
    print(create_pet('Clifford', 'Dog', 32))
    print(Pet('Polly', 'Parrot'))

#this is meant to practice classes and objects in python

class Animal:
    def __init__(self, name, species,sound):
        self.name = name
        self.species = species
        self.sound = sound

    #define a function class called domestic and assign it to inherite the animal quality
    def domestic(self):
        self.sound = "bark"


    #define a function called wild and assign it to inheritance the animal quality
    def wild(self):
        self.sound = "roar"


#define a variable one called pet and and another for the zoo
Pet = Animal("Thanos", "Dog", "Woof")
Pet.domestic()

#print the function in domestic and wild
print(f" These is my pet {Pet.name}, it is a {Pet.species} and it {Pet.sound}")


Zoo = Animal("Dracula", "Lion", "Roar")
Zoo.wild()
print(f" This is wild zoo animal {Zoo.name}, it is a {Zoo.species} and it {Zoo.sound}")
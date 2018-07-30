#!/usr/bin/env python3
from model import PetFamily, PetType, User


teste = PetFamily.all()

if teste:
    exit()

user = User.get_or_create("Foo Zeen", "foo@bar.com", "teste")

dog_detail = """
The domestic dog is a member of the genus canines,
 which forms part of the wolf-like canids and is
 the most widely abundant terrestrial carnivore.
"""
dog = PetFamily.create("Dog", dog_detail, "dog.jpg")

cat_detail = """
Cats are similar in anatomy to the other felids,
 with a strong flexible body, quick reflexes,
 sharp retractable claws and teeth adapted to killing small prey.
"""
cat = PetFamily.create("Cat", cat_detail, "cat.jpg")

bird_detail = """
Birds, are a group of endothermic vertebrates,
 characterised by feathers, toothless beaked jaws,
 the laying of hard-shelled eggs.
"""
bird = PetFamily.create("Bird", bird_detail, "bird.jpg")

rabbit_detail = """
Rabbits are small mammals in the family Leporidae
 of the order Lagomorpha. Oryctolagus cuniculus includes
 the European rabbit species and its descendants.
"""
rabbit = PetFamily.create("Rabbit", rabbit_detail, "rabbit.png")

foobar_detail = """
The terms foobar (/ˈfuːbɑːr/), or foo and others
 are used as placeholder names
 (also referred to as metasyntactic variables) in computer programming or
 computer-related documentation.[1]
 They have been used to name entities such as variables, functions,
 and commands whose exact identity is unimportant
 and serve only to demonstrate a concept.
"""

PetType.create("Foo Dog", foobar_detail, user.id, dog.id)
PetType.create("Foo Cat", foobar_detail, user.id, cat.id)
PetType.create("Foo Bird", foobar_detail, user.id, bird.id)
PetType.create("Foo Rabbit", foobar_detail, user.id, rabbit.id)

types = {"Cat": cat, "Dog": dog, "Bird": bird, "Rabbit": rabbit}
generic_names = ["Thunder", "Lion", "Domestic", "Titan", "Hunter", "Donnie"]

for t in types:
    for name in generic_names:
        name = "%s %s" % (name, t)
        PetType.create(name, foobar_detail, user.id, types[t].id)

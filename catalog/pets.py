#!/usr/bin/env python3
from model import Base, PetFamily, PetType, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('postgresql:///catalog')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user = User(name="Foo Zeen", email="foo@bar.com", picture="teste")
session.add(user)

dog_detail = """
The domestic dog is a member of the genus canines,
 which forms part of the wolf-like canids and is
 the most widely abundant terrestrial carnivore.
"""
dog = PetFamily(name="Dog", picture="dog.jpg", detail=dog_detail)
session.add(dog)

cat_detail = """
Cats are similar in anatomy to the other felids,
 with a strong flexible body, quick reflexes,
 sharp retractable claws and teeth adapted to killing small prey.
"""
cat = PetFamily(name="Cat", picture="cat.jpg", detail=cat_detail)
session.add(cat)

bird_detail = """
Birds, are a group of endothermic vertebrates,
 characterised by feathers, toothless beaked jaws,
 the laying of hard-shelled eggs.
"""
bird = PetFamily(name="Bird", picture="bird.jpg", detail=bird_detail)
session.add(bird)

rabbit_detail = """
Rabbits are small mammals in the family Leporidae
 of the order Lagomorpha. Oryctolagus cuniculus includes
 the European rabbit species and its descendants.
"""
rabbit = PetFamily(name="Rabbit", picture="rabbit.jpg", detail=rabbit_detail)
session.add(rabbit)

foobar_detail = """
The terms foobar (/ˈfuːbɑːr/), or foo and others
 are used as placeholder names
 (also referred to as metasyntactic variables) in computer programming or
 computer-related documentation.[1]
 They have been used to name entities such as variables, functions,
 and commands whose exact identity is unimportant
 and serve only to demonstrate a concept.
"""

foodog = PetType(user=user, name="Foo Dog", detail=foobar_detail,
                 family=dog)
foocat = PetType(user=user, name="Foo Cat", detail=foobar_detail,
                 family=cat)
foobird = PetType(user=user, name="Foo Bird", detail=foobar_detail,
                  family=bird)
foorabbit = PetType(user=user, name="Foo Rabbit", detail=foobar_detail,
                    family=rabbit)

session.add(foodog)
session.add(foocat)
session.add(foobird)
session.add(foorabbit)

types = {"Cat": cat, "Dog": dog, "Bird": bird, "Rabbit": rabbit}
generic_names = ["Thunder", "Lion", "Domestic", "Titan", "Hunter", "Donnie"]

for t in types:
    for name in generic_names:
        name = "%s %s" % (name, t)
        pet = PetType(user=user, name=name, detail=foobar_detail,
                      family=types[t])
        session.add(pet)


session.commit()

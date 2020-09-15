import mongoengine as me
import json
from .film import Films
from .starships import Starships
from .vehicles import Vehicles
from .planets import Planets

class Character(me.Document):
    name = me.StringField(required=True)
    height = me.StringField(required=True)
    mass = me.StringField(required=True)
    birth_year = me.StringField(required=True)
    gender = me.StringField(required=True)
    homeworld = me.StringField(required=True)
    films = me.ListField(me.StringField(), required=True)
    starships = me.ListField(me.StringField())
    vehicles = me.ListField(me.StringField())
    planets = me.ListField(me.StringField())
    url = me.StringField(required=True)

    @classmethod
    def get_all(cls):
        return cls.objects()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(id=id)

    @classmethod
    def add(cls, name,height,mass,birth_year,gender, url, films, starships, vehicles, homeworld):
        cls(
            name=name,
            height=height,
            mass=mass,
            birth_year=birth_year,
            gender=gender,
            homeworld=homeworld,
            url=url,
            films=[Films.get_by_url(film).to_json() for film in films],
            starships=[Starships.get_by_url(starship).to_json() for starship in starships],
            vehicles=[Vehicles.get_by_url(vehicle).to_json() for vehicle in vehicles],
            planets=[Planets.get_by_url(homeworld).to_json()]
        ).save()

        

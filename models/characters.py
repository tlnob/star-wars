import mongoengine as me
import json

class Character(me.Document):
    person_id = me.IntField(required=True, unique=True)
    name = me.StringField(required=True, unique=True)
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
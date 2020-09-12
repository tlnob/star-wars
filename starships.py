import mongoengine as me

class Starships(me.Document):
    name = me.StringField(required=True, unique=True)
    model = me.StringField(required=True)
    manufacturer = me.StringField(required=True)
    cost_in_credits = me.StringField(required=True)
    length = me.StringField(required=True)
    max_atmosphering_speed = me.StringField(required=True)
    crew = me.StringField(required=True)
    passengers = me.StringField(required=True)
    cargo_capacity = me.StringField(required=True)
    consumables = me.StringField(required=True)
    hyperdrive_rating = me.StringField(required=True)
    MGLT = me.StringField(required=True)
    starship_class = me.StringField(required=True)
    calc = me.FloatField(required=True)
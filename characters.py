import mongoengine as me

class Character(me.Document):
    name = me.StringField(required=True, unique=True)
    height = me.StringField(required=True)
    mass = me.StringField(required=True)
    hair_color = me.StringField(required=True)
    skin_color = me.StringField(required=True)
    eye_color = me.StringField(required=True)
    birth_year = me.StringField(required=True)
    gender = me.StringField(required=True)
    homeworld = me.StringField(required=True)
    films = me.ListField(required=True)

    @classmethod
    def add(self, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, films):
        self.name = name
        self.height = height
        self.mass = mass
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.eye_color = eye_color
        self.birth_year = birth_year
        self.gender = gender
        self.homeworld = homeworld
        self.films = films
        try:
            self.save()
        except Exception as e:
            pass
import mongoengine as me

class Vehicles(me.Document):
    name = me.StringField(required=True, unique=True)
    url = me.StringField(required=True)

    @classmethod
    def get_all(cls):
        return cls.objects()

    @classmethod
    def get_by_url(cls, url):
        return cls.objects(url=url)
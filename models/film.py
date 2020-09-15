import mongoengine as me

class Films(me.Document):
    episode_id = me.IntField(required=True, unique=True)
    title = me.StringField()
    url = me.StringField()

    @classmethod
    def get_all(cls):
        return cls.objects()

    @classmethod
    def get_by_url(cls, url):
        return cls.objects(url=url)
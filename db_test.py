class User(Document):
    username = StringField(required=True, max_length=30)
    email = EmailField(required=True)
    watch_list = ListField(ReferenceField(User))
    
class WatchItem(Document):
    name = StringField(required=True)
    date_first_release = DateTimeField(required=False)
    author = ReferenceField(User)

    meta = {'allow_inheritance': True}

class ConsoleWatchItem(WatchItem):
    generation = IntField(required=False)
    abbreviation_official = StringField(required=False)
    developer = ReferenceField(Company)
    name_group = ReferenceField(NameGroup)
    name_prefix = StringField(required=False)
    name_suffix = StringField(required=False)
    name_alternatives = ListField(StringField(max_length=60))
    variations = ListField(ReferenceField(Variation))
    is_external_storage_compatible = BooleanField()

class GameWatchItem(WatchItem):
    platforms = ListField(ReferenceField(User))
    is_bootleg = BooleanField(default=False)

class Company(Document):
    name = StringField(required=True)

class NameGroup(Document):
    name = StringField(required=True)

class Variation(Document):
    name = StringField(required=True)
    model_no = StringField(required=False)
    storage = EmbeddedDocumentListField(Storage)
    editions = EmbeddedDocumentListField(Edition)

class Storage(Document):
    capacity = IntField(required=True)
    unit = StringField(required=False, max_length=2)
    style = StringField(required=False, max_length=30)

class Edition(Document):
    name = StringField(required=False)

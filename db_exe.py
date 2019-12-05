import datetime
from db_models import *
from mongoengine import *
# from pymongo import MongoClient

# client = MongoClient()

# db = client.boardwatch
# users = db.users
# new_user_id = users.insert_one({
#     'name': 'new',
#     'email': 'address@domain.tld'
# }).inserted_id
# print(new_user_id)

connect('boardwatch')

first_watch_item = ConsoleWatchItem(name='console1', date_first_release=datetime.datetime.utcnow(), generation=8, abbreviation_official='PS4', developer='Sony', name_group='PlayStation', name_suffix='4', name_alternatives=[], variations=[], is_external_storage_compatible=True)

first_user = User(username='yaboiiiiii', email='yaboi@yadomain.yb', watch_list=[first_watch_item])

# print(first_user)

for user in User.objects:
    print('user')
    print(user.email)
for console in ConsoleWatchItem.objects:
    print('console')
    print(console.name)
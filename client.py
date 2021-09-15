import pymongo

client = pymongo.MongoClient(host="localhost", port=27017)
coffee = client.coffee
users = coffee.users


print(users)
#print(coffee.list_collection_names())
#print(users.insert_one({"name": "new_name", "id": "new_id"}))
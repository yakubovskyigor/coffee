from pymongo import MongoClient

client = MongoClient(host="Localhost", port=27017)
coffee = client.coffee
users = coffee.users

print(users)
#print(users.insert_one({"name": "new_name", "id": "new_id"}))
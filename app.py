from flask import Flask, request, jsonify, redirect, session, url_for
import pymongo
import bcrypt



app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient(host="localhost", port=27017)
coffee = client.coffee
users = coffee.users
orders = coffee.orders


@app.route('/')
def index_page():
    return "Главная страница"


@app.route('/orders')
def order():
    return "Заказы"


@app.route('/add', methods=['GET', 'POST'])
def add():
    photo = request.form["photo"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    password = request.form["password"]
    phone_number = request.form["phone_number"]
    email = request.form["email"]
    date_of_birth = request.form["date_of_birth"]
    gender = request.form["gender"]
    user_info = dict(first_name=first_name, last_name=last_name, password=password, phone_number=phone_number,
                     email=email, photo=photo, date_of_birth=date_of_birth, gender=gender)
    users.insert_one(user_info)
    return jsonify(message="User added successfully")


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        return jsonify({"response": "Get Request Called"})
    elif request.method == "POST":
        req_Json = request.json
        name = req_Json['name']
        return jsonify({"response": "Hi " + name})


@app.route('/logged_in', methods=["POST"])
def logged_in():
    email = request.form["email"]
    check = users.find_one({"email": email})
    if check:
        return jsonify(message="User Exist")
    else:
        photo = request.form["photo"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        date_of_birth = request.form["date_of_birth"]
        gender = request.form["gender"]
        user_info = dict(first_name=first_name, last_name=last_name, password=password, phone_number=phone_number,
                         email=email, photo=photo, date_of_birth=date_of_birth, gender=gender)
        users.insert_one(user_info)
        return jsonify(message="User added successfully")


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    check = users.find_one({"email": email, "password": password})
    if check:
        return jsonify(message="You are registered")


if __name__ == "__main__":
    app.run(debug=True)



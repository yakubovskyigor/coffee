from flask import Flask, request, jsonify, redirect, session, url_for
import pymongo
import bcrypt



app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient(host="localhost", port=27017)
coffee = client.coffee
users = coffee.users

@app.route('/')
def index_page():
    return "Главная страница"


@app.route('/orders')
def order():
    return "Заказы"


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        return jsonify({"response": "Get Request Called"})
    elif request.method == "POST":
        req_Json = request.json
        name = req_Json['name']
        return jsonify({"response": "Hi " + name})


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = users.find_one({"name": user})
        email_found = users.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return jsonify(message=message)
        if email_found:
            message = 'This email already exists in database'
            return jsonify(message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return jsonify(message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            users.insert_one(user_input)

            user_data = users.find_one({"email": email})
            new_email = user_data['email']

            return jsonify(email=new_email)
    return redirect(url_for('/'))


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return jsonify(email=email)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = users.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return jsonify(message=message)
        else:
            message = 'Email not found'
            return jsonify(message=message)
    return jsonify(message=message)


if __name__ == "__main__":
    app.run(debug=True)
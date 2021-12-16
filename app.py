from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from flask import Flask, request, jsonify, redirect, session, url_for, json
from oauthlib.oauth2 import WebApplicationClient
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token
from flask_login import logout_user
from flask_mail import Mail, Message
from flask_cors import CORS


app = Flask(__name__)
jwt = JWTManager(app)
app.secret_key = "development key"
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "igorby8881@gmail.com"
app.config['MAIL_PASSWORD'] = "i5526678"
cluster = MongoClient(host="localhost", port=27017)
coffee = cluster.coffee
users = coffee.users
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)
mail = Mail(app)
CORS(app)


@app.route('/')
def index_page():
    return "Главная страница"


@app.route('/add', methods=['GET', 'POST'])
def add():
    photo = request.json["photo"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    phone_number = request.json["phone_number"]
    email = request.json["email"]
    date_of_birth = request.json["date_of_birth"]
    gender = request.json["gender"]
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


"Регистрация"


@app.route('/registration', methods=["POST"])
def registration():
    email = request.json["email"]
    check = users.find_one({"email": email})
    if check:
        return jsonify(message="User Exist")
    else:
        email = request.json["email"]
        password = request.json["password"]

        user_info = dict(email=email, password=password)
        users.insert_one(user_info)
        # access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify(message="User added successfully", refresh_token=refresh_token, user=email), 200


"Авторизация"


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.json["email"]
        password = request.json["password"]

    check = users.find_one({"email": email, "password": password})
    if check:
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify(message="Пользователь с таким именем зарегистрирован", access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify(message="Неверный логин или пароль"), 401


"""Заказ"""


@app.route("/order", methods=['post', 'get', 'put'])
def order():
    user_id = request.json["_id"]
    order_data = {
        "order_number": request.json["order_number"],
        "type_of_coffee": request.json["type_of_coffee"],
        "price": request.json["price"],
        "quantity": request.json["quantity"],
        "additions": request.json["additions"],
            }
    coffee.users.update(
        {"_id": ObjectId(user_id)},
        {"$set": {'order_data': order_data}}
    )
    return jsonify("Заказ принят")


# "GOOGLE регистрация"
#
#
# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()
#
#
# @app.route("/login_google")
# def login_google():
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)
#
#
# @app.route("/login/callback")
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")
#
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )
#
#     # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))
#
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#
#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400


"""Подсчет количества пользователей"""


@app.route("/users_count")
def users_count():
    count = coffee.users.count()
    return jsonify(count)


"""US03-03 Переход по разделам меню"""


@app.route("/menu_point", methods=["POST"])
def menu_point():
    menu = {
        "coffee": request.json["coffee"],
        "hot_drinks": request.json["hot_drinks"]
    }
    return jsonify(menu)


# @app.route("/send", methods=['post', 'get'])
# def send_mail():
#     msg = Message(subject="Смена статуса заказа",
#                   sender='igorby8881@gmail.com', recipients=["igorby@mail.ru"])
#     msg.body = "Уважаемый пользователь!"
#     mail.send(msg)
#     return jsonify(message="ghhh")
#
#
# """Выход"""
#
#
# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

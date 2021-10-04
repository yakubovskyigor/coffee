import requests
from flask import Flask, request, jsonify, redirect, session, url_for
import pymongo
from bson.objectid import ObjectId
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient(host="localhost", port=27017)
coffee = client.coffee
users = coffee.users
orders = coffee.orders
CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'coffee'


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


@app.route('/logged_in', methods=["POST"])
def logged_in():
    email = request.json["email"]
    check = users.find_one({"email": email})
    if check:
        return jsonify(message="User Exist")
    else:
        email = request.json["email"]
        password = request.json["password"]
        photo = request.json["photo"]
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        phone_number = request.json["phone_number"]
        date_of_birth = request.json["date_of_birth"]
        gender = request.json["gender"]
        user_info = dict(first_name=first_name, last_name=last_name, password=password, phone_number=phone_number,
                         email=email, photo=photo, date_of_birth=date_of_birth, gender=gender)
        users.insert_one(user_info)
        return jsonify(message="User added successfully")


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
        return jsonify(message="You are registered")


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
        {"$push": {'order_data': order_data}}
    )
    return jsonify("Заказ принят")


"GOOGLE регистрация"


@app.route('/test_api')
def test_api_request():
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, credentials=credentials)

    files = drive.files().list().execute()

    session['credentials'] = credentials_to_dict(credentials)

    return jsonify(**files)


@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback(credentials=None):
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('test_api_request'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
      **session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.')
    else:
        return('An error occurred.')


@app.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']
    return('Credentials have been cleared.<br><br>')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


if __name__ == "__main__":
    app.run(debug=True)



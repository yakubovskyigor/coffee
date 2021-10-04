from flask import Flask, request, jsonify, redirect, session, url_for
import pymongo
import app


class User():
    photo = request.json["photo"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    phone_number = request.json["phone_number"]
    email = request.json["email"]
    date_of_birth = request.json["date_of_birth"]
    gender = request.json["gender"]


#class Order(User):
    photo = User.photo
    first_name = User.first_name
    last_name = User.last_name
    phone_number = User.phone_number
    email = User.email


#@app.route("/OrderItem", methods=["POST"])
#class OrderItem(Order):
    type_of_coffee: dict
    price: float
    quantity: int
    additions: dict

    def __init__(self, type_of_coffee, quantity, additions, price):
        self.type_of_coffee = type_of_coffee
        self.price = price
        self.quantity = quantity
        self.additions = additions

    def get_cost(self):
        return self.price * self.quantity




u = User
o = Order
oi = OrderItem(("Cappuccino", "Americano", "Latte"), 2, ("1", "2"), 10.5)
print(oi.get_cost())

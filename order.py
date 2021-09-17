from flask import Flask, request, jsonify, redirect, session, url_for
import pymongo
from app import orders


class User():
    photo = "photo"
    first_name = "first_name"
    last_name = "last_name"
    password = "password"
    phone_number = "phone_number"
    email = "email"
    date_of_birth = "date_of_birth"
    gender = "gender"


class Order(User):
    photo = User.photo
    first_name = User.first_name
    last_name = User.last_name
    phone_number = User.phone_number
    email = User.email
    created = "принят"
    work = "в работе"
    ready = "готов"
    received = "получен"


class OrderItem(Order):
    type_of_coffee = "Вид кофе"
    price = "Цена"
    quantity = "Количество"
    additions = dict

    def __init__(self, type_of_coffee, price, quantity, additions):
        self.type_of_coffee = type_of_coffee
        self.price = price
        self.quantity = quantity
        self.additions = additions

    def get_cost(self):
        return self.price * self.quantity




u = User
o = Order
oi = OrderItem
print(o.phone_number)

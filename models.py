from collections import namedtuple
from peewee import *
from playhouse.flask_utils import FlaskDB

db = FlaskDB()

class User(db.Model):
    email: TextField(primary_key=True)
    firstName: TextField()
    lastName: TextField()
    password: TextField()
    role: TextField()

class Product(db.Model):
    code: TextField(primary_key=True)
    name: TextField()
    description: TextField()
    price: IntegerField()
    stock: IntegerField()
    state: TextField() ## 0: inactive, 1: active

class CommentsCalifications(db.Model):
    id: IntegerField(primary_key=True)
    userEmail: ForeignKeyField(User)
    productCode: ForeignKeyField(Product)
    content: TextField()
    calification: IntegerField()
    date: TextField()
    state: TextField() ## 0: inactive, 1: active

class Wishes(db.Model):
    id: IntegerField(primary_key=True)
    userEmail: ForeignKeyField(User)
    productCode: ForeignKeyField(Product)
    state: TextField() ## 0: inactive, 1: active

class Purchases(db.Model):
    id: IntegerField(primary_key=True)
    userEmail: ForeignKeyField(User)
    date: TextField()

class PurchasedProducts(db.Model):
    id: IntegerField(primary_key=True)
    purchaseId: ForeignKeyField(Purchases)
    productCode: ForeignKeyField(Product)
    price: IntegerField()
    quantity: IntegerField()
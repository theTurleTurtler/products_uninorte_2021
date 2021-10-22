from collections import namedtuple
from peewee import *
from playhouse.flask_utils import FlaskDB

db = FlaskDB()

class User(db.Model):
    id: IntegerField(primary_key=True)
    email: TextField()
    firstName: TextField()
    lastName: TextField()
    password: TextField()
    role: TextField()

class Product(db.Model):
    id: IntegerField(primary_key=True)
    name: TextField()
    description: TextField()
    price: IntegerField()
    stock: IntegerField()
    state: TextField() ## 0: inactive, 1: active

class CommentsCalifications(db.Model):
    id: IntegerField(primary_key=True)
    userId: ForeignKeyField(User)
    productId: ForeignKeyField(Product)
    content: TextField()
    calification: IntegerField()
    date: TextField()
    state: TextField() ## 0: inactive, 1: active

class Wishes(db.Model):
    id: IntegerField(primary_key=True)
    userId: ForeignKeyField(User)
    productId: ForeignKeyField(Product)
    state: TextField() ## 0: inactive, 1: active

class Purchases(db.Model):
    id: IntegerField(primary_key=True)
    userId: ForeignKeyField(User)
    date: TextField()

class PurchasedProducts(db.Model):
    id: IntegerField(primary_key=True)
    purchaseId: ForeignKeyField(Purchases)
    productId: ForeignKeyField(Product)
    price: IntegerField()
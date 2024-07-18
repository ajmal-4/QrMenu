from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://ajmalpn1007:aju110077@clusterqrmenu.wh3aqpl.mongodb.net/?retryWrites=true&w=majority&appName=ClusterQrMenu"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('mongotry')
special_items = db.get_collection('special_items')
categories = db.get_collection('categories')
items = db.get_collection('items')
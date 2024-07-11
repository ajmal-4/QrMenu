from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

class SpecialItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

if __name__ == '__main__':
    with app.app_context():
        categories = Category.query.all()
        special_items = SpecialItem.query.all()

        print("Categories:")
        for category in categories:
            print(f"Category: {category.name}")
            for item in category.items:
                print(f"- Item: {item.name}, Price: {item.price}, Description: {item.description}")

        print("\nSpecial Items:")
        for special_item in special_items:
            print(f"Special Item: {special_item.name}, Price: {special_item.price}, Description: {special_item.description}")

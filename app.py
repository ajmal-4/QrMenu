from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for google cloud host
from dotenv import load_dotenv
import os
from flask_cors import CORS

# for google cloud host
load_dotenv()

app = Flask(__name__)
# for google cloud host
CORS(app)

# for google cloud host
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Categories of the Menu (Each Category have Id,Name and Items)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)
# Items of the menu (Each item corresponds to any one category. Items have Id, Category Id, Name, price, and its description)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)


# Special Item
class SpecialItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

# Admin Page
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        # For Adding a Category 
        if 'category_name' in request.form:
            category_name = request.form['category_name']
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
        # For adding an item
        elif 'item_name' in request.form and 'item_id' not in request.form:
            item_name = request.form['item_name']
            item_price = request.form['item_price']
            item_description = request.form['item_description']
            category_id = request.form['category_id']
            new_item = Item(name=item_name, price=item_price, description=item_description, category_id=category_id)
            db.session.add(new_item)
            db.session.commit()
        # For editing an existing item
        elif 'item_id' in request.form:
            item_id = request.form['item_id']
            item = Item.query.get(item_id)
            item.name = request.form['item_name']
            item.price = request.form['item_price']
            item.description = request.form['item_description']
            item.category_id = request.form['category_id']
            db.session.commit()
        # For updating category name
        elif 'update_category_id' in request.form:
            update_category_id = request.form['update_category_id']
            new_category_name = request.form['new_category_name']
            category = Category.query.get(update_category_id)
            if category:
                category.name = new_category_name
                db.session.commit()
        # Special Item
        elif 'special_item_name' in request.form and 'special_item_id' not in request.form:
            special_item_name = request.form['special_item_name']
            special_item_price = request.form['special_item_price']
            special_item_description = request.form['special_item_description']
            new_special_item = SpecialItem(name=special_item_name, price=special_item_price, description=special_item_description)
            db.session.add(new_special_item)
            db.session.commit()
        elif 'special_item_id' in request.form:
            special_item_id = request.form['special_item_id']
            special_item = SpecialItem.query.get(special_item_id)
            special_item.name = request.form['special_item_name']
            special_item.price = request.form['special_item_price']
            special_item.description = request.form['special_item_description']
            db.session.commit()
        
        return redirect(url_for('admin'))
    
    categories = Category.query.all()
    special_items = SpecialItem.query.all()

    # For populating the items for editing
    item_to_edit = None

    special_item_to_edit = None

    if 'edit_item_id' in request.args:
        item_to_edit = Item.query.get(request.args['edit_item_id'])

    if 'edit_special_item_id' in request.args:
        special_item_to_edit = SpecialItem.query.get(request.args['edit_special_item_id'])
    
    # Rendering the admin template
    return render_template('admin.html',categories=categories,item_to_edit=item_to_edit,special_items=special_items,special_item_to_edit=special_item_to_edit)


# For deleting an item
@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('admin'))


# For updating the Category Name
@app.route('/update_category/<int:category_id>', methods=['POST'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if category:
        new_category_name = request.form['new_category_name']
        category.name = new_category_name
        db.session.commit()
    return redirect(url_for('admin'))
# For deleting a Category(Only if it has no items left)
@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category and len(category.items) == 0:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for('admin'))


@app.route('/delete_special_item/<int:special_item_id>', methods=['POST'])
def delete_special_item(special_item_id):
    special_item = SpecialItem.query.get(special_item_id)
    if special_item:
        db.session.delete(special_item)
        db.session.commit()
    return redirect(url_for('admin'))


@app.route('/')
def home():
    categories = Category.query.all()
    special_items = SpecialItem.query.all()
    return render_template('menu.html',categories=categories,special_items=special_items)



if __name__ == '__main__':
    app.run()

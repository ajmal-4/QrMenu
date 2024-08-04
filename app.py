from flask import Flask,render_template,request,redirect,url_for
# To retrieve object id - Mongodb database
from bson.objectid import ObjectId
# Importing file db - database setup for mongodb
import db

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

# Home Page - Menu Page
@app.route('/')
def home():
    categories = list(db.categories.find())

    for category in categories:
        category['_id'] = str(category['_id'])  # Convert ObjectId to string for Jinja
        category['items'] = list(db.items.find({'category_id': category['_id']}))  # Retrieve items for each category

    special_items = list(db.special_items.find())

    return render_template('menu.html', categories=categories, special_items=special_items)

# Admin Page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # For Adding a Category
        if 'category_name' in request.form:
            category_name = request.form['category_name']
            db.categories.insert_one({'name': category_name})
        # For adding an item
        elif 'item_name' in request.form and 'item_id' not in request.form:
            item_name = request.form['item_name']
            item_price = request.form['item_price']
            item_description = request.form['item_description']
            category_id = request.form['category_id']
            db.items.insert_one({'name': item_name, 'price': float(item_price), 'description': item_description, 'category_id': category_id})
        # For editing an existing item
        elif 'item_id' in request.form:
            item_id = ObjectId(request.form['item_id'])
            db.items.update_one(
                {'_id': item_id},
                {'$set': {
                    'name': request.form['item_name'],
                    'price': float(request.form['item_price']),
                    'description': request.form['item_description'],
                    'category_id': request.form['category_id']
                }}
            )
        # For updating category name
        elif 'update_category_id' in request.form:
            update_category_id = ObjectId(request.form['update_category_id'])
            new_category_name = request.form['new_category_name']
            db.categories.update_one(
                {'_id': update_category_id},
                {'$set': {'name': new_category_name}}
            )
        # For adding or updating special items
        elif 'special_item_name' in request.form:
            special_item_name = request.form['special_item_name']
            special_item_price = request.form['special_item_price']
            special_item_description = request.form['special_item_description']
            if 'special_item_id' in request.form:
                special_item_id = ObjectId(request.form['special_item_id'])
                db.special_items.update_one(
                    {'_id': special_item_id},
                    {'$set': {
                        'name': special_item_name,
                        'price': float(special_item_price),
                        'description': special_item_description
                    }}
                )
            else:
                db.special_items.insert_one({
                    'name': special_item_name,
                    'price': float(special_item_price),
                    'description': special_item_description
                })
        
        return redirect(url_for('admin'))
    
    categories = list(db.categories.find())
    special_items = list(db.special_items.find())
    items = list(db.items.find())

     # Add item count to each category
    for category in categories:
        category['_id'] = str(category['_id'])
        category['items_count'] = db.items.count_documents({'category_id': ObjectId(category['_id'])})

    # For populating the items for editing
    item_to_edit = None
    special_item_to_edit = None

    if 'edit_item_id' in request.args:
        item_to_edit = db.items.find_one({'_id': ObjectId(request.args['edit_item_id'])})

    if 'edit_special_item_id' in request.args:
        special_item_to_edit = db.special_items.find_one({'_id': ObjectId(request.args['edit_special_item_id'])})
    
    return render_template('admin.html', categories=categories, item_to_edit=item_to_edit, special_items=special_items, special_item_to_edit=special_item_to_edit,items=items)

@app.route('/delete_item/<item_id>', methods=['POST'])
def delete_item(item_id):
    db.items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('admin'))

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    new_category_name = request.form['new_category_name']
    db.categories.update_one({'_id': ObjectId(category_id)}, {'$set': {'name': new_category_name}})
    return redirect(url_for('admin'))

@app.route('/delete_category/<category_id>', methods=['POST'])
def delete_category(category_id):
    category_id = ObjectId(category_id)
    category = db.categories.find_one({'_id': category_id})
    if category and db.items.count_documents({'category_id': category_id}) == 0:
        db.categories.delete_one({'_id': category_id})
    return redirect(url_for('admin'))

@app.route('/delete_special_item/<special_item_id>', methods=['POST'])
def delete_special_item(special_item_id):
    db.special_items.delete_one({'_id': ObjectId(special_item_id)})
    return redirect(url_for('admin'))

# Supplier Function
@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    if request.method == 'POST':
        table_number = request.form['table_number']
        ordered_items = request.form.getlist('items')
        # Here you would typically save the order to the database
        db.orders.insert_one({'table_number': table_number, 'items': ordered_items})
        return redirect(url_for('supplier'))
    
    categories = list(db.categories.find())
    for category in categories:
        category['_id'] = str(category['_id'])  # Convert ObjectId to string for Jinja
        category['items'] = list(db.items.find({'category_id': category['_id']}))  # Retrieve items for each category

    
    return render_template('supplier_orders.html', categories=categories)


if __name__ == '__main__':
    app.run()

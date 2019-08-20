"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Book
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/books', methods=['GET','POST'])
def books():

    # POST request
    if request.method == 'POST':
        body = request.get_json()
        book1 = Book(name=body['name'], title=body['title'], person_id=body['person_id'])
        db.session.add(book1)
        db.session.commit()
        return "ok", 200
# GET request
    if request.method == 'GET':
        all_books = Book.query.all()
        all_books = list(map(lambda x: x.serialize(), all_books))
        return jsonify(all_books), 200



@app.route('/users', methods=['GET','POST'])
def handle_person():
     # POST request
    if request.method == 'POST':
        body = request.get_json()
        user1 = Person(name=body['name'], email=body['email'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200



# ADD TO INSOMNIA
# add many books to the person_id = 1
# {
# 	"name": "ghghghg",
# 	"title":"hgkugkkgfhjf",
# 	"person_id": 1
# }




# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)

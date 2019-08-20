from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    books = db.relationship("Book",  lazy=True) #takes class name books uppercase

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "books": list(map(lambda x: x.serialize(), self.books)),
            "id": self.id
        }

class Book (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(120), unique=True, nullable=False)
    person_id = db.Column(db.Integer,db.ForeignKey('person.id'), nullable=False)



    def serialize(self):
        return {
            "name": self.name,
            "title": self.title,
        }
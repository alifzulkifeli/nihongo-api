import os
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import Response

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "nihongo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    meaning = db.Column(db.String)
    explaination = db.Column(db.String)
    example = db.Column(db.String)

    def __repr__(self):
        return f"<Book(word={self.word}, meaning={self.meaning}, explaination={self.explaination}, example={self.example})>"

    def toDict(self):
        return {
            "id": self.id,
            "word": self.word,
            "meaning": self.meaning,
            "explaination": self.explaination,
            "example": self.example
        }


# ROUTE

@app.route('/', methods=["GET", "POST"])
def home():
    return "Flask REST API Boilerplate v1.0"


@app.route('/add', methods=["GET", "POST"])
def add():
    books = None
    if request.json:
        try:
            book = Book(word=request.json['word'], meaning=request.json['meaning'],
                        explaination=request.json['explaination'], example=request.json['example'])
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add")
            print(e)
            return(("Failed to add")), 400
    return book.toDict()


@app.route('/read', methods=["GET"])
def read():
    if request.json:
        try:
            book = Book.query.get(request.json["id"])
            db.session.commit()
            print(book.toDict())
            return book.toDict()
        except Exception as e:
            print("Failed to add")
            print(e)
            return(("Failed to add")), 400


@app.route("/update", methods=["POST"])
def update():
    try:
        book = Book.query.get(request.json["id"])

        book.word = request.json['word']
        book.meaning = request.json['meaning']
        book.explaination = request.json['explaination']
        book.example = request.json['example']

        db.session.commit()
        return book.toDict()
    except Exception as e:
        print(e)
        return("Couldn't update "), 400


@app.route("/delete", methods=["DELETE"])
def delete():
    try:
        book = Book.query.get(request.json["id"])
        db.session.delete(book)
        db.session.commit()
        return "Deleted"
    except Exception as e:
        print(e)
        return ("Couldn't delete "), 400



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

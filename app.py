from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/warezgeeks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db.init_app(app)
Migrate(app, db)


@app.route("/login", methods=["POST"])
def login():
    user = User.query.get(1)
    return jsonify(user.serialize_just_username())

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
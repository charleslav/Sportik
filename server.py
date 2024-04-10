from flask import Flask, render_template, Response, jsonify, request

from flask_cors import CORS, cross_origin

from database import Database

import uuid

myDatabase = Database()

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
@cross_origin()
def index():
    return jsonify({"message": "Hello World!"})

@app.route("/login", methods=["POST"])
@cross_origin()
def getUser():
    data = request.json
    cid = myDatabase.get_user(data["username"], data["password"])
    if cid is None:
        return jsonify({"status": "400", "message": "Invalid username or password"})
    response = {
        "status" : 200,
        "cid" : cid,
        "token" : uuid.uuid4()
    }
    return jsonify(response)

@app.route("/register", methods=["POST"])
@cross_origin()
def registerUser():
    return null

@app.route("/products", methods=["GET"])
@cross_origin()
def getAllProducts():
    data = myDatabase.get_products()
    response = {
        "products" : data,
        "status" : 200
    }
    return jsonify(response)
if __name__ == '__main__':
    app.run()

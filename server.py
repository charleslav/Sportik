from flask import Flask, render_template, Response, jsonify, request

from flask_cors import CORS, cross_origin

from database import Database

import uuid

myDatabase = Database()

app = Flask(__name__)
cors = CORS(app)
CORS(app, origins='http://localhost:8080', allow_headers=['Content-Type'])

@app.route("/")
def index():
    return jsonify({"message": "Hello World!"})


@app.route("/login", methods=["POST"])
def getUser():
    data = request.json
    cid = myDatabase.get_user(data["username"], data["password"])[0]
    if cid is None:
        return jsonify({"status": "400", "message": "Invalid username or password"})

    my_uuid = str(uuid.uuid4())

    myDatabase.set_token(my_uuid, cid)


    response = {
        "status": 200,
        "cid": cid,
        "token": my_uuid
    }
    return jsonify(response)


@app.route("/register", methods=["POST"])
def registerUser():
    body = request.json
    myDatabase.insert_customer(body["name"],
                               body["username"], body["password"],
                               body["age"], body["email"],
                               body["address"])

    response = {
        "status": 200,
        "token": uuid.uuid4()
    }
    return jsonify(response)


@app.route("/brands", methods=["GET"])
def getAllProducts():
    data = myDatabase.get_products()
    response = {
        "brands": data,
        "status": 200
    }
    return jsonify(response)

@app.route("/brands/<brand_id>", methods=["GET"])
def getBrandModelByBrand(brand_id):
    data = myDatabase.get_brand_id(brand_id)
    response = {
        "brandModel": data,
        "status": 200
    }
    return jsonify(response)

@app.route("/product/<int:id>", methods=["GET"])
def getProductById(id):
    data = myDatabase.get_products_by_id(id)
    response = {
        "productData": data[0],
        "status": 200
    }
    return jsonify(response)

@app.route("/information/<int:idModel>", methods=["GET"])
def getInformationById(idModel):
    data = myDatabase.get_information_by_model_id(idModel)
    response = {
        "modelData": data[0],
        "status": 200
    }
    return jsonify(response)

@app.route("/review", methods=["POST"])
def addReview():
    body = request.get_json()
    customerId = myDatabase.get_customer_id_from_token(body["customer_token"])[0]["customerId"]
    myDatabase.add_review(customerId, body["brand_model_id"], body["comment"], body["rating"]);
    response = {
        "status": 200
    }
    return jsonify(response)

@app.route("/cart", methods=["POST"])
def addToCart():
    body = request.get_json()
    try:
        customerId = verifyToken(body["token"]);
    except:
        return jsonify()
    body = request.get_json()
    getToken(body["token"])


@app.route("/token/<string:token>", methods=["GET"])
def getToken(token):
    try:
        customerId = verifyToken(token)
        response = {
            "status": 200,
            "customerId": customerId
        }
    except Exception as e:
        response = {
            "status": 401
        }
    return jsonify(response)

def verifyToken(token):
    return myDatabase.get_customer_id_from_token(token)[0]["customerId"]


@app.route("/review/<int:bmid>", methods=["GET"])
def getReviewForModel(bmid):

    reviews = myDatabase.get_review_for_model(bmid)
    response = {
        "status": 200,
        "reviews": reviews
    }
    myJson = jsonify(response)
    return myJson



if __name__ == '__main__':
    app.run(threaded=True)

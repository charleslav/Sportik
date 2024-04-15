import pymysql
import uuid
from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS, cross_origin

from database import Database
from pymysql import OperationalError, DataError, IntegrityError
from hashlib import sha256
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
    try:
        cid = myDatabase.get_user(data["username"], sha256(data["password"].encode('utf-8')).hexdigest())[0]
    except TypeError :
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
    try:
        cid = myDatabase.insert_customer(body["name"],
                               body["username"], sha256(body["password"].encode("utf-8")).hexdigest(),
                               body["age"], body["email"],
                               body["address"])
        token = uuid.uuid4()
        myDatabase.set_token(token, cid)
        response = {
            "status": 200,
            "token": token
        }
    except DataError as err:
        if err.args[0] == 1264:
            response = {
                "status": 401,
                "message": "Votre âge n'est pas conforme à nos normes"
            }
    except IntegrityError as err:
        if err.args[0] == 1062:
            response = {
                "status": 401,
                "message": "Votre mail est déjà enregistré"
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
        response = {
            "status": 401,
            "message": "Your are not login or your session expired"
        }
        return jsonify(response)
    try:
        var = myDatabase.add_to_cart(customerId, body["bmid"], body["quantity"])
        response = {
            "status": 200
        }
        return jsonify(response)
    except OperationalError as e:
        if (e.args[0] == 1644):
            response = {
                "status": 401,
                "message": "Your card already have been added"
            }
            return jsonify(response)
    except Exception as e:
        response = {
            "status": 401,
            "message": "Something went wrong"
        }
        return jsonify(response)

    return jsonify(response)

@app.route("/cart/<string:token>", methods=["GET"])
def getCart(token):
    try:
        customerId = verifyToken(token);
        try:
            data = myDatabase.get_cart(customerId);

            response = {
                "status": 200,
                "cart": data
            }
        except Exception as e:
            response = {
                "status": 401,
                "message": "Something went wrong"
            }
    except:
        response = {
            "status": 401,
            "message": "Your are not login or your session expired"
        }


    return jsonify(response)


@app.route("/cart/quantity", methods=["PUT"])
def updateQuantity():
    body = request.get_json()
    try:
        customerId = verifyToken(body["token"]);
    except:
        response = {
            "status": 401,
            "message": "Your are not login or your session expired"
        }
    try:
        data = myDatabase.update_quantity_cart(customerId, body["bmid"], body["quantity"])
        response = {
            "status": 200}
    except Exception as e:
        response = {
            "status": 401,
            "message": "Something went wrong"
        }
    jsonResponse = jsonify(response)
    return jsonResponse


@app.route("/user/<string:token>/cart/<int:bmid>", methods=["DELETE"])
def deleteCart(token, bmid):
    try:
        customerId = verifyToken(token);
        myDatabase.delete_cart(customerId, bmid)
        response = {"status": 200}
        return jsonify(response)
    except:
        response = {
            "status": 401,
            "message": "Your are not login or your session expired"
        }

@app.route("/user/<string:token>/checkout", methods=["GET"])
def getCheckout(token):
    try:
        customerId = verifyToken(token)
        data = myDatabase.get_checkout(customerId)[0]
        response = {
            "status": 200,
            "checkout_data": data}

    except Exception as e:
        response = {
            "status": 401,
            "message": "Your are not login or your session expired"
        }
    return jsonify(response)

@app.route("/user/<string:token>/place_order", methods=["POST"])
def add_order(token):
    try:
        body = request.get_json()
        customerId = verifyToken(token)
        myDatabase.place_order(body["payment_method"], customerId)
        response = {
            "status": 200,
            }

    except Exception as e:
        response = {
            "status": 401,
            "message": "Your are not login or your session expired"
        }
    return jsonify(response)

@app.route("/token/<string:token>", methods=["GET"])
def getToken(token):
    try:
        customerId = verifyToken(token)
        response = {
            "status": 200,
            "customerId": customerId
        }
    except OperationalError as e:
        response = {
            "status": 401
        }
    except Error as e:
        response = {}
    return jsonify(response)

def verifyToken(token):
    return myDatabase.get_customer_id_from_token(token)[0]["customer_id"]


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

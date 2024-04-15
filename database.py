import os
import random
from datetime import datetime

import cursor
from faker import Faker

import pymysql
from dotenv import load_dotenv
from pymysql import IntegrityError


# from sql_utils import run_sql_file

class Dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
class Database:
    def __init__(self):
        """
            Chargez les variables denvironnement de votre fichier .env, puis complétez les lignes 15 à 19 afin de récupérer les valeurs de ces variables
        """
        load_dotenv()
        self.host = os.environ.get("HOST")
        self.port = os.environ.get("PORT")
        self.database = os.environ.get("DATABASE")
        self.user = os.environ.get("USER")
        self.password = os.environ.get("PASSWORD")

        self._open_sql_connection()

        self.migration_counter = 0

    def _open_sql_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=int(self.port),
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True
        )

        self.cursor = self.connection.cursor()

    def get_results(self):
        desc = [d[0] for d in self.cursor.description]
        results = [Dotdict(dict(zip(desc, res))) for res in self.cursor.fetchall()]
        return results

    def set_token(self, token, cid):
        request = f"""INSERT INTO token (token, customer_id) VALUES ('{token}',{cid})"""
        self.cursor.execute(request)
    def get_user(self, username, password):
        request = f"""SELECT cid FROM sportik.customer WHERE username = '{username}' AND password = '{password}'"""
        self.cursor.execute(request)
        response = self.cursor.fetchone()
        return response

    def insert_customer(self, name, username, password, age, email, customer_adress):
        request = f"""INSERT INTO sportik.customer (name, username, password, age, email, customer_adress) VALUES ('{name}','{username}','{password}',{age},'{email}','{customer_adress}')"""
        self.cursor.execute(request)
        # Assuming you're using MySQL, you can use "cursor.lastrowid" to get the last inserted ID directly.
        last_inserted_id = self.cursor.lastrowid
        return last_inserted_id

    def get_products(self):
        request = f"""SELECT * from brand"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_brand_id(self, brand_id):
        request = f"""SELECT * FROM brand_model INNER JOIN sportik.brand_model_image on brand_model.bmid = sportik.brand_model_image.brand_model_id WHERE brand_model.brand_id = '{brand_id}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_products_by_id(self, id):
        request = f"""SELECT * from product WHERE pid = '{id}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_information_by_model_id(self, id):
        request = f"""SELECT * FROM brand_model INNER JOIN sportik.brand_model_image on brand_model.bmid = sportik.brand_model_image.brand_model_id WHERE brand_model.bmid = '{id}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_customer_id_from_token(self, token):
        request = f"""SELECT customer_id FROM token WHERE token = '{token}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def add_review(self, customer_id, bmid, comment, rating):
        request = f"""INSERT INTO customer_review (customer_id, brand_model_id, brand_rating_review) VALUES ({customer_id}, {bmid}, '{rating}')"""
        self.cursor.execute(request)

    def get_review_for_model(self, bmid):
        request = f"""SELECT * FROM customer_review WHERE brand_model_id = {bmid}"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def add_to_cart(self, customer_id, bmid, quantity):
        requestBrandModel = f"""SELECT price, discount_id FROM brand_model WHERE bmid = {bmid}"""
        self.cursor.execute(requestBrandModel)
        response = self.get_results()
        price = response[0]["price"]
        discount_id = response[0]["discount_id"]

        if discount_id is not None:
            requestDiscountTotal = f"""SELECT discount_rate FROM discount WHERE did = {discount_id}"""
            self.cursor.execute(requestDiscountTotal)
            response = self.get_results()
            discount_rate = response[0]["discount_rate"]
        else:
            discount_rate = 0

        request = f"""INSERT INTO cart (cid, brand_model_id, quantity, order_total, order_total_discount) VALUES ({customer_id}, {bmid}, {quantity}, {price}, {discount_rate})"""
        self.cursor.execute(request)

    def place_order(self, payment_method, customerId):
        request = f"""INSERT INTO orders (payment_method, payment_status) VALUES ('{payment_method}', 'Succes')"""
        requestDelete = f"""DELETE FROM cart WHERE cid = {customerId}"""
        requestCheckoutId = f"""SELECT checkout_id from checkout WHERE customer_id = {customerId}"""
        self.cursor.execute(requestCheckoutId)
        checkout_id = self.get_results()[0]["checkout_id"]
        requestUpdate = f"""CALL updateStockQuantityAfterPurchase({checkout_id})"""
        self.cursor.execute(requestUpdate)
        self.cursor.execute(request)
        self.cursor.execute(requestDelete)

    def get_cart(self, customerId):
        request = f"""SELECT cart.brand_model_id, cid, cart.quantity, brand_model.price, brand_model.quantity AS stock, 
            brand_model.brand_model_name, brand_model_image.image
            FROM Cart
            INNER JOIN Brand_Model
            ON Cart.brand_model_id = Brand_Model.bmid
            INNER JOIN brand_model_image
            on Brand_Model.bmid = brand_model_image.brand_model_id WHERE cid = {customerId} AND image_type = "main";"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def update_quantity_cart(self, customerId, bmid, quantity):
        request = f"""UPDATE Cart SET quantity = {quantity} WHERE brand_model_id = {bmid} AND cid = {customerId};"""
        self.cursor.execute(request)

    def delete_cart(self, customerId, bmid):
        request = f"""DELETE FROM cart WHERE brand_model_id = {bmid} AND cid = {customerId};"""
        self.cursor.execute(request)

    def get_checkout(self, customerId):
        request = f"""SELECT * FROM checkout WHERE customer_id = {customerId};"""
        self.cursor.execute(request)
        response = self.get_results()
        requestUpdate = f"""CALL updateCheckout({response[0].checkout_id});"""
        self.cursor.execute(requestUpdate)
        request = f"""SELECT * FROM checkout WHERE customer_id = {customerId};"""
        self.cursor.execute(request)
        response = self.get_results()

        return response


def generate_customer_data(cursor, fake):
    for i in range(100):
        name = fake.unique.name()
        username = fake.unique.user_name()
        password = fake.password()
        email = fake.unique.email()
        age = random.randint(16, 127)
        customer_adress = fake.address()
        request = f"""INSERT INTO Customer (name, username, password, age, email, customer_adress)
            VALUES("{name}", '{username}', '{password}', '{age}', '{email}', '{customer_adress}');"""
        cursor.execute(request)


def generate_product_data(cursor):
    products = [
        {
            "brand_name": "Jordan",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/61089404-82a0-4adb-a6c2-a88ae94b76c1/chaussure-air-jordan-1-elevate-high-pour-kFQLcG.png",
            "description": "Air Jordan is a renowned line of basketball shoes and athletic clothing produced by Nike. It was created for former NBA player Michael Jordan and released to the public on April 1, 1985. The shoes were designed by Peter Moore, Tinker Hatfield, and Bruce Kilgore, and are known for their innovative design, performance, and cultural impact."
        },
        {
            "brand_name": "Adidas",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/15f901c90a9549d29104aae700d27efb_9366/Chaussure_Superstar_noir_EG4959_01_standard.jpg",
            "description": "Adidas AG is a German athletic apparel and footwear corporation headquartered in Herzogenaurach, Bavaria, Germany. It is the largest sportswear manufacturer in Europe, and the second largest in the world, after Nike."
        },
        {
            "brand_name": "Under Armour",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://underarmour.scene7.com/is/image/Underarmour/3025516-003_DEFAULT?rp=standard-30pad%7CpdpMainDesktop&scl=1&fmt=jpg&qlt=85&resMode=sharp2&cache=on%2Con&bgc=f0f0f0&wid=566&hei=708&size=536%2C688",
            "description": "Under Armour, Inc. is an American sportswear company that manufactures footwear and apparel headquartered in Baltimore, Maryland, United States."
        },
        {
            "brand_name": "Puma",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://m.media-amazon.com/images/I/51CVBOSNjoL._AC_SY575_.jpg",
            "description": "Puma SE is a German multinational corporation that designs and manufactures athletic and casual footwear, apparel, and accessories, headquartered in Herzogenaurach, Bavaria, Germany. Puma is the third largest sportswear manufacturer in the world."
        },
        {
            "brand_name": "New Balance",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://nb.scene7.com/is/image/NB/wl574evw_nb_02_i?$pdpflexf2$&wid=440&hei=440",
            "description": "New Balance is one of the worlds major sports footwear and apparel manufacturers. Based in Boston, Massachusetts, the multinational corporation was founded in 1906 as the New Balance Arch Support Company."
        },
        {
            "brand_name": "Reebook",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://m.media-amazon.com/images/I/51KqpzgpztS._AC_SY575_.jpg",
            "description": "Reebok International Limited is an American footwear and clothing company founded in Bolton, England, and headquartered in Boston, Massachusetts."
        },
        {
            "brand_name": "Fila",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://m.media-amazon.com/images/I/61K2k-8GKZL._AC_UY900_.jpg",
            "description": "Fila is an Italian-South Korean sporting goods company founded in 1911 in Biella, Italy, and now based in Seoul."
        },
        {
            "brand_name": "Vans",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://m.media-amazon.com/images/I/71bsjxWjrxL._AC_UY900_.jpg",
            "description": "Vans is an American manufacturer of skateboarding shoes and related apparel, based in Santa Ana, California, owned by VF Corporation."
        },
        {
            "brand_name": "Asics",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://i.ebayimg.com/images/g/ryAAAOSwgMdlKROA/s-l1200.webp",
            "description": "Asics is a Japanese multinational corporation which produces sports equipment designed for a wide range of sports."
        },
        {
            "brand_name": "Brooks",
            "brand_rating": random.randint(0, 5),
            "brand_image": "https://m.media-amazon.com/images/I/81FC5MZk8SL._AC_UY900_.jpg",
            "description": "Brooks is an American athletic footwear brand known for its innovative designs and high-performance running shoes. Founded in 1914, Brooks has a long history of providing runners with comfortable and durable footwear engineered to enhance performance and prevent injury. Whether youre a seasoned marathoner or a casual jogger, Brooks shoes are designed to provide optimal support, cushioning, and stability to help you achieve your running goals. With a commitment to quality and innovation, Brooks continues to be a trusted choice for runners of all levels around the world."
        }
    ]

    for product in products:
        request = f"""INSERT INTO Brand (brand_name, brand_rating, brand_image, description)
        VALUES('{product["brand_name"]}', {product["brand_rating"]}, '{product["brand_image"]}', '{product["description"]}');"""
        cursor.execute(request)


def generate_product_model_data(cursor):
    brands = [
        {
            "name": "Jordan",
            "models": [
                {
                    "brand_model_name": "Air Jordan 1",
                    "price": random.randint(150, 300),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000000,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Air Jordan 3",
                    "price": random.randint(150, 300),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000000,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Air Jordan 5",
                    "price": random.randint(150, 300),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000000,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Adidas",
            "models": [
                {
                    "brand_model_name": "Adidas Superstar",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000001,
                    "discount_id": 4000000,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Adidas Stan Smith",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000001,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Adidas Ultraboost",
                    "price": random.randint(150, 250),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000001,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Under Armour",
            "models": [
                {
                    "brand_model_name": "Under Armour HOVR Sonic",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000002,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Under Armour Curry 7",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000002,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Under Armour SpeedForm Apollo",
                    "price": random.randint(100, 180),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000002,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Puma",
            "models": [
                {
                    "brand_model_name": "Puma Clyde",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000003,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Puma Suede",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000003,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Puma RS-X",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000003,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "New Balance",
            "models": [
                {
                    "brand_model_name": "New Balance 990",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000004,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "New Balance 574",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000004,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "New Balance Fresh Foam 1080",
                    "price": random.randint(150, 250),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000004,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Reebok",
            "models": [
                {
                    "brand_model_name": "Reebok Classic Leather",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000005,
                    "discount_id": 4000000,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Reebok Nano X",
                    "price": random.randint(100, 180),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000005,
                    "discount_id": 4000000,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Reebok Club C",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000005,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Fila",
            "models": [
                {
                    "brand_model_name": "Fila Disruptor II",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000006,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Fila Ray Tracer",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000006,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Fila Mindblower",
                    "price": random.randint(100, 180),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000006,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Vans",
            "models": [
                {
                    "brand_model_name": "Vans Old Skool",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000007,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Vans Authentic",
                    "price": random.randint(50, 100),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000007,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Vans Sk8-Hi",
                    "price": random.randint(70, 130),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000007,
                    "discount_id": 4000003,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Asics",
            "models": [
                {
                    "brand_model_name": "Asics Gel-Kayano 27",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000008,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Asics Gel-Nimbus 23",
                    "price": random.randint(150, 250),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000008,
                    "discount_id": 4000000,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Asics Gel-Resolution 8",
                    "price": random.randint(130, 220),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000008,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Brooks",
            "models": [
                {
                    "brand_model_name": "Brooks Ghost 13",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000009,
                    "discount_id": "Null",
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Brooks Adrenaline GTS 21",
                    "price": random.randint(130, 220),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000009,
                    "discount_id": 4000002,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "brand_model_name": "Brooks Glycerin 19",
                    "price": random.randint(140, 230),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000009,
                    "discount_id": 4000002,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        }
    ]

    for brand in brands:
        for model in brand["models"]:
            request = f"""INSERT INTO Brand_Model (brand_model_name, price, quantity, discount_id, packaging_id, brand_id)
            VALUES('{model["brand_model_name"]}', {model["price"]}, {model["quantity"]}, {model["discount_id"]},{model["packaging_id"]}, {model["product_id"]});"""
            cursor.execute(request)

def generate_brand_model_image(cursor):
    brand_model_ids = list(range(8000000, 8000030))
    image_urls = [
        "https://cdn-images.farfetch-contents.com/13/15/76/97/13157697_21516295_600.jpg",
        "https://i.ebayimg.com/images/g/0oYAAOSwKS1jHHqN/s-l1200.jpg",
        "https://static.nike.com/a/images/t_prod_ss/w_960,c_limit,f_auto/e0083865-8eb4-47d4-8404-e2dd9e767513/date-de-sortie-de-la-air-jordan%C2%A05-%C2%AB%C2%A0racer-blue%C2%A0%C2%BB-ct4838-004.jpg",
        "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/f74a314d42b2411db478e2e0a2c2c7c4_9366/Superstar_Shoes_Blue_IF1581_01_standard.jpg",
        "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/e01dea68cf93434bae5aac0900af99e8_9366/Chaussure_Stan_Smith_blanc_FX5500_01_standard.jpg",
        "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/c608f554cb3b4d12b392af000188c513_9366/Chaussure_Ultraboost_1.0_noir_HQ4199_01_standard.jpg",
        "https://underarmour.scene7.com/is/image/Underarmour/3024898-001_DEFAULT?rp=standard-30pad%7CpdpMainDesktop&scl=1&fmt=jpg&qlt=85&resMode=sharp2&cache=on%2Con&bgc=f0f0f0&wid=566&hei=708&size=536%2C688",
        "https://cdn-images.farfetch-contents.com/20/17/10/58/20171058_50032045_600.jpg",
        "https://ca.shop.runningroom.com/media/catalog/product/cache/453c4871d8f4dcbe6098dec5e744d96c/_/1/_1245952_m_b_r_1.jpg",
        "https://i.ebayimg.com/images/g/RrwAAOSwV9Nk-KJJ/s-l1200.webp",
        "https://m.media-amazon.com/images/I/51dHwNeY9LL._AC_UY900_.jpg",
        "https://media.sneakerpricer.com/media/puma-chaussure-sneakers-rs-x-soft-femme-rose-pearlpink-393772_05-a205709b-c92a-4521-864a-06a6a7d0513e_thumbnail_2x_jpeg.jpg",
        "https://nb.scene7.com/is/image/NB/m990gl6_nb_02_i?$pdpflexf2$&wid=440&hei=440",
        "https://nb.scene7.com/is/image/NB/gc574evw_nb_02_i?$dw_detail_gallery$",
        "https://ca.shop.runningroom.com/media/catalog/product/cache/623252543a71a417af50138275bda2d9/m/1/m1080g11_2.jpg",
        "https://reebok.ca/cdn/shop/products/GY0960B0020_3e5cfc71-f936-4ac4-a59b-ea252a46607a.jpg?v=1667960570",
        "https://m.media-amazon.com/images/I/61O8ZrQHx8L._AC_UY900_.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRm0GmsyGqeiUfVTXna1u6XOlLQIh41M8ofQ3mstNsnWQ&s",
        "https://images.journeys.ca/images/products/1_457372_FS_HERO.JPG",
        "https://m.media-amazon.com/images/I/71LjtMLJ2RL._AC_UY900_.jpg",
        "https://i.ebayimg.com/images/g/E6kAAOSwq5BcukNt/s-l1200.webp",
        "https://m.media-amazon.com/images/I/71bsjxWjrxL._AC_UY900_.jpg",
        "https://images.vans.com/is/image/Vans/VN000EE3_BKA_HERO?wid=800&hei=1004&fmt=jpeg&qlt=50&resMode=sharp2&op_usm=0.9,1.5,8,0",
        "https://cdn.skatepro.com/product/520/vans-skate-sk8-hi-shoes-g5.webp",
        "https://images.asics.com/is/image/asics/1011A767_001_SR_RT_GLB?$sfcc-product$",
        "https://m.media-amazon.com/images/I/61KViYUcC6L._AC_UY900_.jpg",
        "https://img.runningwarehouse.com/watermark/rsg.php?path=/content_images/reviews/Brooks_Adrenaline_21/Brooks_Adrenaline_21-R1.jpg&nw=728",
        "https://lecoureurnordique.ca/cdn/shop/products/brooks-glycerin-19-femme-le-coureur-nordique-29_700x700.jpg?v=1668745697",
        "https://shopsolescience.ca/cdn/shop/products/Glycerin-19-Ombre-Violet-Lavender-45_600x.jpg?v=1621026027",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQt0BL-yHrsA8CTja_rz_pLk6q3rkLHfz1tEN-GwpGhAw&s"

    ]
    index = 0
    for brand_model_id in brand_model_ids:
            image_url = image_urls[index]
            request = f"""INSERT INTO Brand_model_image (brand_model_id, image_type, image)
                            VALUES({brand_model_id}, 'main', '{image_url}');"""
            cursor.execute(request)
            print(index)
            index = index + 1

def generate_product_packaging_data(cursor):
    for i in range(30):
        dimension = random.choice(["50x50x50", "60x60x60", "70x70x70","80x80x80","90x90x90", "100x100x100"])
        weight = random.randint(1, 100)
        packaging_material = random.choice(["Cardboard boxes", "Corrugated boxes"])
        request = f"""INSERT INTO Product_Packaging (dimension, weight, packaging_material)
        VALUES("{dimension}", {weight}, "{packaging_material}");"""
        cursor.execute(request)

def generate_provider_data(cursor, fake):
    for i in range(5):
        provider_name = fake.company()
        is_featured = random.randint(0, 1)
        featured_image = "Sportik/images/" + provider_name + ".png"
        request = f"""INSERT INTO Provider (provider_name, is_featured, featured_image)
        VALUES("{provider_name}", {is_featured}, "{featured_image}");"""
        cursor.execute(request)

def generate_discount_data(cursor, fake):
    for i in range(5):
        discount_rate = random.randint(0, 100)
        dateIsValid = False
        while not dateIsValid:
            start_date = fake.date_this_year(before_today=True, after_today=True)
            end_date = fake.date_this_year(before_today=False, after_today=True)
            if start_date <= end_date:
                dateIsValid = True
        is_active = 0
        if(start_date <= datetime.now().date()):
            is_active = 1

        request = f"""INSERT INTO Discount (discount_rate, start_date, end_date, is_active)
        VALUES({discount_rate}, "{start_date}", "{end_date}", {is_active});"""
        cursor.execute(request)

def generate_provider_data(cursor, fake):
    for i in range(5):
        provider_name = fake.company()
        is_featured = random.randint(0, 1)
        featured_image = "Sportik/images/" + provider_name + ".png"
        request = f"""INSERT INTO Provider (provider_name, is_featured, featured_image)
        VALUES("{provider_name}", {is_featured}, "{featured_image}");"""
        cursor.execute(request)

if __name__ == '__main__':
    db = Database()  # Create an instance of the Database class
    create_table = "CREATE TABLE todo(id INTEGER AUTO_INCREMENT, text VARCHAR(400), PRIMARY KEY(id));"
    fake = Faker()
    cursor = db.cursor  # Access the cursor from the Database instance
    generate_customer_data(cursor, fake)
    generate_discount_data(cursor, fake)
    generate_product_data(cursor)
    generate_product_model_data(cursor)
    generate_provider_data(cursor, fake)
    generate_brand_model_image(cursor)
    cursor.execute(create_table)

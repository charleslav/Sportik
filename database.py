import os
import random
from datetime import datetime

import cursor
from faker import Faker

import pymysql
from dotenv import load_dotenv
from pymysql import IntegrityError


# from sql_utils import run_sql_file

class dotdict(dict):
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
        results = [dotdict(dict(zip(desc, res))) for res in self.cursor.fetchall()]
        return results

    def set_token(self, token, cid):
        request = f"""INSERT INTO token (token, customerId) VALUES ('{token}',{cid})"""
        self.cursor.execute(request)
    def get_user(self, username, password):
        request = f"""SELECT cid FROM sportik.customer WHERE username = '{username}' AND password = '{password}'"""
        self.cursor.execute(request)
        response = self.cursor.fetchone()
        return response

    def insert_customer(self, name, username, password, age, email, customer_adress):
        request = f"""INSERT INTO sportik.customer (name, username, password, age, email, customer_adress) VALUES ('{name}','{username}','{password}',{age},'{email}','{customer_adress}')"""

        self.cursor.execute(request)

    def get_products(self):
        request = f"""SELECT * from brand"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_brand_id(self, brand_id):
        request = f"""SELECT * FROM brand_model WHERE brand_id = '{brand_id}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_products_by_id(self, id):
        request = f"""SELECT * from product WHERE pid = '{id}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_information_by_model_id(self, id):
        request = f"""SELECT * FROM brand_model WHERE bmid = '{id}'"""
        self.cursor.execute(request)
        response = self.get_results()
        return response

    def get_customer_id_from_token(self, token):
        request = f"""SELECT customerId FROM token WHERE token = '{token}'"""
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
            "brand_image": "Sportik/images/Jordan.png",
            "description": "Air Jordan is a renowned line of basketball shoes and athletic clothing produced by Nike. It was created for former NBA player Michael Jordan and released to the public on April 1, 1985. The shoes were designed by Peter Moore, Tinker Hatfield, and Bruce Kilgore, and are known for their innovative design, performance, and cultural impact."
        },
        {
            "brand_name": "Adidas",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Adidas.png",
            "description": "Adidas AG is a German athletic apparel and footwear corporation headquartered in Herzogenaurach, Bavaria, Germany. It is the largest sportswear manufacturer in Europe, and the second largest in the world, after Nike."
        },
        {
            "brand_name": "Under Armour",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Under_Armour.png",
            "description": "Under Armour, Inc. is an American sportswear company that manufactures footwear and apparel headquartered in Baltimore, Maryland, United States."
        },
        {
            "brand_name": "Puma",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Puma.png",
            "description": "Puma SE is a German multinational corporation that designs and manufactures athletic and casual footwear, apparel, and accessories, headquartered in Herzogenaurach, Bavaria, Germany. Puma is the third largest sportswear manufacturer in the world."
        },
        {
            "brand_name": "New Balance",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/New_Balance.png",
            "description": "New Balance is one of the worlds major sports footwear and apparel manufacturers. Based in Boston, Massachusetts, the multinational corporation was founded in 1906 as the New Balance Arch Support Company."
        },
        {
            "brand_name": "Reebook",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Reebook.png",
            "description": "Reebok International Limited is an American footwear and clothing company founded in Bolton, England, and headquartered in Boston, Massachusetts."
        },
        {
            "brand_name": "Fila",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Fila.png",
            "description": "Fila is an Italian-South Korean sporting goods company founded in 1911 in Biella, Italy, and now based in Seoul."
        },
        {
            "brand_name": "Vans",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Vans.png",
            "description": "Vans is an American manufacturer of skateboarding shoes and related apparel, based in Santa Ana, California, owned by VF Corporation."
        },
        {
            "brand_name": "Asics",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Asics.png",
            "description": "Asics is a Japanese multinational corporation which produces sports equipment designed for a wide range of sports."
        },
        {
            "brand_name": "Brooks",
            "brand_rating": random.randint(0, 5),
            "brand_image": "Sportik/images/Brooks.png",
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
    cursor.execute(create_table)

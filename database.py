import os
import random
from datetime import datetime

import cursor
from faker import Faker

import pymysql
from dotenv import load_dotenv


# from sql_utils import run_sql_file


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

    def get_user(self, username, password):
        request = f"""SELECT cid FROM sportik.customer WHERE username = '{username}' AND password = '{password}'"""
        self.cursor.execute(request)
        response = self.cursor.fetchone()
        return response


def insert_todo(text):
    request = f"""INSERT INTO todo (text) VALUE ("{text}")"""

    cursor.execute(request)



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
            "product_name": "Jordan",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Jordan.png",
            "description": "Air Jordan is a renowned line of basketball shoes and athletic clothing produced by Nike. It was created for former NBA player Michael Jordan and released to the public on April 1, 1985. The shoes were designed by Peter Moore, Tinker Hatfield, and Bruce Kilgore, and are known for their innovative design, performance, and cultural impact."
        },
        {
            "product_name": "Adidas",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Adidas.png",
            "description": "Adidas AG is a German athletic apparel and footwear corporation headquartered in Herzogenaurach, Bavaria, Germany. It is the largest sportswear manufacturer in Europe, and the second largest in the world, after Nike."
        },
        {
            "product_name": "Under Armour",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Under_Armour.png",
            "description": "Under Armour, Inc. is an American sportswear company that manufactures footwear and apparel headquartered in Baltimore, Maryland, United States."
        },
        {
            "product_name": "Puma",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Puma.png",
            "description": "Puma SE is a German multinational corporation that designs and manufactures athletic and casual footwear, apparel, and accessories, headquartered in Herzogenaurach, Bavaria, Germany. Puma is the third largest sportswear manufacturer in the world."
        },
        {
            "product_name": "New Balance",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/New_Balance.png",
            "description": "New Balance is one of the worlds major sports footwear and apparel manufacturers. Based in Boston, Massachusetts, the multinational corporation was founded in 1906 as the New Balance Arch Support Company."
        },
        {
            "product_name": "Reebook",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Reebook.png",
            "description": "Reebok International Limited is an American footwear and clothing company founded in Bolton, England, and headquartered in Boston, Massachusetts."
        },
        {
            "product_name": "Fila",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Fila.png",
            "description": "Fila is an Italian-South Korean sporting goods company founded in 1911 in Biella, Italy, and now based in Seoul."
        },
        {
            "product_name": "Vans",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Vans.png",
            "description": "Vans is an American manufacturer of skateboarding shoes and related apparel, based in Santa Ana, California, owned by VF Corporation."
        },
        {
            "product_name": "Asics",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Asics.png",
            "description": "Asics is a Japanese multinational corporation which produces sports equipment designed for a wide range of sports."
        },
        {
            "product_name": "Brooks",
            "product_rating": random.randint(0, 5),
            "product_image": "Sportik/images/Brooks.png",
            "description": "Brooks is an American athletic footwear brand known for its innovative designs and high-performance running shoes. Founded in 1914, Brooks has a long history of providing runners with comfortable and durable footwear engineered to enhance performance and prevent injury. Whether youre a seasoned marathoner or a casual jogger, Brooks shoes are designed to provide optimal support, cushioning, and stability to help you achieve your running goals. With a commitment to quality and innovation, Brooks continues to be a trusted choice for runners of all levels around the world."
        }
    ]

    for product in products:
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product["product_name"]}', {product["product_rating"]}, '{product["product_image"]}', '{product["description"]}');"""
        cursor.execute(request)


def generate_product_model_data(cursor):
    brands = [
        {
            "name": "Jordan",
            "models": [
                {
                    "product_name": "Air Jordan 1",
                    "price": random.randint(150, 300),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000000,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Air Jordan 3",
                    "price": random.randint(150, 300),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000000,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Air Jordan 5",
                    "price": random.randint(150, 300),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000000,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Adidas",
            "models": [
                {
                    "product_name": "Adidas Superstar",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000001,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Adidas Stan Smith",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000001,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Adidas Ultraboost",
                    "price": random.randint(150, 250),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000001,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Under Armour",
            "models": [
                {
                    "product_name": "Under Armour HOVR Sonic",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000002,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Under Armour Curry 7",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000002,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Under Armour SpeedForm Apollo",
                    "price": random.randint(100, 180),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000002,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Puma",
            "models": [
                {
                    "product_name": "Puma Clyde",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000003,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Puma Suede",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000003,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Puma RS-X",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000003,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "New Balance",
            "models": [
                {
                    "product_name": "New Balance 990",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000004,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "New Balance 574",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000004,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "New Balance Fresh Foam 1080",
                    "price": random.randint(150, 250),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000004,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Reebok",
            "models": [
                {
                    "product_name": "Reebok Classic Leather",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000005,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Reebok Nano X",
                    "price": random.randint(100, 180),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000005,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Reebok Club C",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000005,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Fila",
            "models": [
                {
                    "product_name": "Fila Disruptor II",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000006,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Fila Ray Tracer",
                    "price": random.randint(80, 150),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000006,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Fila Mindblower",
                    "price": random.randint(100, 180),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000006,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Vans",
            "models": [
                {
                    "product_name": "Vans Old Skool",
                    "price": random.randint(60, 120),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000007,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Vans Authentic",
                    "price": random.randint(50, 100),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000007,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Vans Sk8-Hi",
                    "price": random.randint(70, 130),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000007,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Asics",
            "models": [
                {
                    "product_name": "Asics Gel-Kayano 27",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000008,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Asics Gel-Nimbus 23",
                    "price": random.randint(150, 250),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000008,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Asics Gel-Resolution 8",
                    "price": random.randint(130, 220),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000008,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        },
        {
            "name": "Brooks",
            "models": [
                {
                    "product_name": "Brooks Ghost 13",
                    "price": random.randint(120, 200),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000009,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Brooks Adrenaline GTS 21",
                    "price": random.randint(130, 220),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000009,
                    "packaging_id": random.randint(3000000, 3000029)
                },
                {
                    "product_name": "Brooks Glycerin 19",
                    "price": random.randint(140, 230),
                    "quantity": random.randint(1, 50),
                    "product_id": 7000009,
                    "packaging_id": random.randint(3000000, 3000029)
                }
            ]
        }
    ]

    for brand in brands:
        for model in brand["models"]:
            request = f"""INSERT INTO Product_Model (product_name, price, quantity, product_id, packaging_id)
            VALUES('{model["product_name"]}', {model["price"]}, {model["quantity"]}, {model["product_id"]}, {model["packaging_id"]});"""
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

def generate_categories_data(cursor):
    categories = [
        {
            "category_name" : "Shoes",
            "parent_category_id" : "NULL",
            "is_active" : 1
        },
        {
            "category_name": "Sport",
            "parent_category_id": 1000000,
            "is_active": 1
        },
        {
            "category_name": "Classic",
            "parent_category_id": 1000000,
            "is_active": 1
        },
        {
            "category_name": "Colorways",
            "parent_category_id": 1000000,
            "is_active": 1
        },
        {
            "category_name": "Basketball",
            "parent_category_id": 1000001,
            "is_active": 1
        },
        {
            "category_name": "Running",
            "parent_category_id": 1000001,
            "is_active": 1
        },
        {
            "category_name": "Casual",
            "parent_category_id": 1000002,
            "is_active": 1
        }
    ]

    for category in categories:
        request = f"""INSERT INTO Category (category_name,parent_category_id, is_active)
        VALUES('{category["category_name"]}', {category["parent_category_id"]}, '{category["is_active"]}');"""
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
    generate_product_data(cursor)
    generate_product_packaging_data(cursor)
    generate_product_model_data(cursor)
    generate_provider_data(cursor, fake)
    generate_categories_data(cursor)
    generate_discount_data(cursor, fake)
    cursor.execute(create_table)

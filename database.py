import os
import random

import cursor
from faker import Faker

import pymysql
from dotenv import load_dotenv

#from sql_utils import run_sql_file


class Database:
    def __init__(self):
        """
            Chargez les variables d'environnement de votre fichier .env, puis complétez les lignes 15 à 19 afin de récupérer les valeurs de ces variables
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
    for i in range(1):
        product_name = "Jordan"
        product_rating = random.randint(0,5)
        product_image = "Sportik/images/Jordan.png"
        description = "Air Jordan is a renowned line of basketball shoes and athletic clothing produced by Nike. It was created for former NBA player Michael Jordan and released to the public on April 1, 1985.The shoes were designed by Peter Moore, Tinker Hatfield, and Bruce Kilgore, and are known for their innovative design, performance, and cultural impact."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Adidas"
        product_rating = random.randint(0,5)
        product_image = "Sportik/images/Adidas.png"
        description = "Adidas AG is a German athletic apparel and footwear corporation headquartered in Herzogenaurach, Bavaria, Germany. It is the largest sportswear manufacturer in Europe, and the second largest in the world, after Nike."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Under Armour"
        product_rating = random.randint(0,5)
        product_image = "Sportik/images/Under_Armour.png"
        description = "Under Armour, Inc. is an American sportswear company that manufactures footwear and apparel headquartered in Baltimore, Maryland, United States. Under Armour, Inc."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Puma"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/Puma.png"
        description = "Puma SE is a German multinational corporation that designs and manufactures athletic and casual footwear, apparel, and accessories, headquartered in Herzogenaurach, Bavaria, Germany. Puma is the third largest sportswear manufacturer in the world."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "New Balance"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/New_Balance.png"
        description = "New Balance is one of the worlds major sports footwear and apparel manufacturers. Based in Boston, Massachusetts, the multinational corporation was founded in 1906 as the New Balance Arch Support Company."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Reebook"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/Reebook.png"
        description = "Reebok International Limited is an American footwear and clothing company founded in Bolton, England, and headquartered in Boston, Massachusetts. Since 2005, the company is subsidiary of German sporting goods giant Adidas. Reebok produces and distributes fitness, running and CrossFit sportswear including clothing and footwear."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Fila"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/Fila.png"
        description = "Fila is an Italian-South Korean sporting goods company founded in 1911 in Biella, Italy, and now based in Seoul."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Vans"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/Vans.png"
        description = "Vans is an American manufacturer of skateboarding shoes and related apparel, based in Santa Ana, California, owned by VF Corporation."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Asics"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/Asics.png"
        description = "Asics is a Japanese multinational corporation which produces sports equipment designed for a wide range of sports."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)
    for i in range(1):
        product_name = "Brooks"
        product_rating = random.randint(0, 5)
        product_image = "Sportik/images/Brooks.png"
        description = "Brooks is an American athletic footwear brand known for its innovative designs and high-performance running shoes. Founded in 1914, Brooks has a long history of providing runners with comfortable and durable footwear engineered to enhance performance and prevent injury. Whether you're a seasoned marathoner or a casual jogger, Brooks shoes are designed to provide optimal support, cushioning, and stability to help you achieve your running goals. With a commitment to quality and innovation, Brooks continues to be a trusted choice for runners of all levels around the world."
        request = f"""INSERT INTO Product (product_name, product_rating, product_image, description)
        VALUES('{product_name}', {product_rating}, '{product_image}', '{description}');"""
        cursor.execute(request)




if __name__ == '__main__':
    db = Database()  # Create an instance of the Database class
    create_table = "CREATE TABLE todo(id INTEGER AUTO_INCREMENT, text VARCHAR(400), PRIMARY KEY(id));"
    fake = Faker()
    cursor = db.cursor  # Access the cursor from the Database instance
    generate_customer_data(cursor, fake)
    generate_product_data(cursor)
    cursor.execute(create_table)


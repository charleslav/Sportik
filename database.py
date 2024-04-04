import os

import cursor
import pymysql
from dotenv import load_dotenv


# from sql_utils import run_sql_file


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


if __name__ == '__main__':
    create_table = "CREATE TABLE todo(id INTEGER AUTO_INCREMENT, text VARCHAR(400), PRIMARY KEY(id));"

    cursor.execute(create_table)
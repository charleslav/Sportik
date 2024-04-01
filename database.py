import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="cheaito",
    db="labo6",
    autocommit=True
)

cursor = connection.cursor()


def insert_todo(text):
    request = f"""INSERT INTO todo (text) VALUE ("{text}")"""

    cursor.execute(request)

if __name__ == '__main__':
    create_table = "CREATE TABLE todo(id INTEGER AUTO_INCREMENT, text VARCHAR(400), PRIMARY KEY(id));"

    cursor.execute(create_table)

from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from psycopg2 import OperationalError
import psycopg2




# host="localhost",database="FaceDb",user="belit",
# password="12897",port="5432"

def create_connection(db_name="FaceDb", db_user="belit", db_password='12897', db_host="localhost",
                               db_port="5432"):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

#euclideon sql
#"INSERT INTO encodes ( name, encode) VALUES ('{}', CUBE(array[{}]))".format(name,','.join(str(s) for s in face_encodings))


def saveDb(name, face_encodings):

    with create_connection() as conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO encodes ( name, encode) VALUES ('{}', CUBE(array[{}]))".format(name, ','.join(str(s) for s in face_encodings))
            cursor.execute(query)
            cursor.close()
            conn.commit()
            print("saved")
            return 1
        except Exception as e:
            conn.rollback()
            print("error", e)
            return 0



def findDb(face_encodings, threshold=0.4):

    with create_connection() as conn:

        try:

            name = 'Unknown'


            cursor = conn.cursor()

            #euclidean distance on sql

            query = "SELECT name FROM encodes WHERE sqrt(power(CUBE(array[{}]) <-> encode, 2)) <= {} ".format(','.join(str(s) for s in face_encodings), threshold) + "ORDER BY sqrt(power(CUBE(array[{}]) <-> encode, 2)) ASC LIMIT 1".format(','.join(str(s) for s in face_encodings))

            cursor.execute(query)

            data = cursor.fetchone()

            if data == None:

                return name

            else:

                return data

        except Exception as e:


            return e


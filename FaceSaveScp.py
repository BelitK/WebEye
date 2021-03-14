from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from psycopg2 import OperationalError
import psycopg2




# host="localhost",database="FaceDb",user="belit",
# password="12897",port="5432"

def create_connection(db_name="FaceDb", db_user="belit", db_password="None", db_host="localhost",
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
            #ToDo change save type from list to psql list
            #query = "INSERT INTO encodes ( name, encode) VALUES ('{}', CUBE(array[{}]))"  .format(name, ','.join(str(s) for s in face_encodings))
            # face_Array=[]
            # for ar in face_encodings:
            #     ar2 = ",".join(str(ar))
            #
            #     face_Array.append(ar2)
            # print(face_Array)
            # str2 = ",".join(list)
            # return ()


            #','.join(str(s) for s in face_encodings)


            #query = f"INSERT INTO encodes (name, encode) VALUES ('{name}','{face_encodings}')"
            query = f"INSERT INTO encodetest (name, encode_low, encode_high) VALUES ('{name}', CUBE(array[{','.join(str(s) for s in face_encodings[0][0:64])}]), CUBE(array[{','.join(str(s) for s in face_encodings[0][64:128])}]))"

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

            #query = f"SELECT name FROM encodetest WHERE sqrt(power(CUBE(array[{','.join(str(s) for s in face_encodings[0][0:64])}]) <-> encode_low, 2) + power(CUBE(array[{','.join(str(s) for s in face_encodings[0][64:128])}]) <-> encode_high, 2)) <= {threshold}"+ f"ORDER BY sqrt(power(CUBE(array[{','.join(str(s) for s in face_encodings[0][0:64])}]) <-> encode_low, 2) + power(CUBE(array[{','.join(str(s) for s in face_encodings[0][64:128])}]) <-> encode_high, 2)) <-> encode_high) ASC LIMIT 1"

            query = f"SELECT name FROM encodetest WHERE sqrt(power(CUBE(array[{','.join(str(s) for s in face_encodings[0][0:64])}]) <-> encode_low, 2) + power(CUBE(array[{','.join(str(s) for s in face_encodings[0][64:128])}]) <-> encode_high, 2)) <= {threshold}" + f"ORDER BY sqrt(power(CUBE(array[{','.join(str(s) for s in face_encodings[0][0:64])}]) <-> encode_low, 2) + power(CUBE(array[{','.join(str(s) for s in face_encodings[0][64:128])}]) <-> encode_high, 2)) <-> encode_high ) ASC LIMIT 1"
            cursor.execute(query)

            data = cursor.fetchone()

            if data == None:
                print(name,"data=none")
                return name

            else:
                print(name,"data=else")
                return data

        except Exception as e:


            return e


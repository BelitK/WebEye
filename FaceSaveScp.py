import psycopg2
from psycopg2 import OperationalError




db = SimpleConnectionPool(1, 10,host=hostname,database=dbname,user=dbuser,
password=dbpass)

@contextmanager
def get_connection():
    con = db.getconn()
    try:
        yield con
    finally:
        db.putconn(con)

def saveDb(employeeId, name, face_encodings):

    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO facedb (employeeid, employeename, encodevector) VALUES ('{}','{}', CUBE(array[{}]))".format(employeeId, name, ','.join(str(s) for s in face_encodings))
            cursor.execute(query)
            cursor.close()
            conn.commit()
            return 1
        except:
            conn.rollback()
            return 0




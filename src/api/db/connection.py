import psycopg2
import psycopg2.extras
import os

# connection details
DB_NAME = os.environ.get('DB_NAME', 'yacs')
DB_USER = os.environ.get('DB_USER', None)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', None)
DB_PASS = os.environ.get('DB_PASS', None)

class database():
    def __init__(self):
        self.conn = None  # No connection initially
    
    def connect(self):
        """Ensures a persistent database connection, reconnecting if necessary."""
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT,
                )
                print("[INFO] Database Connected")
            except psycopg2.Error as e:
                print("[ERROR] Database connection failed:", e)
                raise

    def close(self):
        """Closes the connection if it is open."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("[INFO] Database Connection Closed")

    def execute(self, sql, args, isSELECT=True):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret = None
        try:
            if isSELECT:
                cur.execute(sql, args)
                ret = cur.fetchall()
            else:
                cur.execute(sql, args)
                ret = 0
                self.conn.commit()

        except psycopg2.Error as e:
            print("DATABASE ERROR: ", end="")
            print(e)
            self.conn.rollback()
            return (ret, e)

        return (ret, None)

    def get_connection(self):
        """Returns a valid connection, ensuring it is active."""
        self.connect()  # Reconnect if needed
        return self.conn


db = database()
db.connect()

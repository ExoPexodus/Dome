import psycopg2
import psycopg2.extras

hostname = "ep-curly-poetry-514695.ap-southeast-1.aws.neon.tech"
database = "neondb"
uname = "rushilrana"
port_id = "5432"
pwd = "izFsjS7GK4rQ"
conn = None
cur = None

def connect():
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=uname,
        password=pwd,
        port=port_id)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("connection successful")
    return cur,conn

def disconnect():
    if conn:
        conn.close()
        cur.close()
        print("successfully disconnected")

def bp():
    print("button pressed")


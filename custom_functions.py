import psycopg2
import psycopg2.extras
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

hostname = config['Postgresql']['host']
database = config['Postgresql']['database']
uname = config['Postgresql']['user']
port_id = config['Postgresql']['port']
pwd = config['Postgresql']['password']
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


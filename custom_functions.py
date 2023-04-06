import psycopg2
import psycopg2.extras
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

hostname = config.get('postgresql','host')
database = config.get('postgresql','database')
uname = config.get('postgresql','user')
port_id = config.get('postgresql','port')
pwd = config.get('postgresql','password')
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


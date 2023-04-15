import psycopg2
import psycopg2.extras
import configparser
import os
from datetime import datetime, timedelta

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

def update_acc_analysis(radio,sql_exp,sql_inc,line_canvas_exp,line_ax_exp,line_canvas_inc,line_ax_inc,date_button_start,date_button_end,uid,text1,text2):
    check_cursor()
    selection = radio.get()
    end_date = datetime.today()
    if selection == 0:
        start_date = end_date - timedelta(days=7)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)

    elif selection == 1:
        start_date = end_date - timedelta(days=30)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)

    elif selection == 2:
        start_date = end_date.replace(day=1)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)

    elif selection == 3:
        start_date = end_date.replace(month=1, day=1)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)

    else:
        start_date = date_button_start.get()
        end_date = date_button_end.get()
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)

cur, conn = connect()

def check_cursor():
    """
    Check if a cursor is closed, and if it is, rollback the connection to restore it.
    """
    if cur.closed:
        cur.connection.rollback()
def line_graph(sql,uid,start_date,end_date,canvas,ax,text):

    ax.clear() # clear previous chart
    # Define a function to fetch data from database
    cur.execute(sql, (start_date, end_date, uid))
    # Create a dictionary to store the data for each transaction type
    data_dict = {
        "Cash": {"x": [], "y": []},
        "Card": {"x": [], "y": []},
        "Savings": {"x": [], "y": []}
    }

    # Fetch the data from the cursor and store it in the dictionary
    for date, amount, transaction_type in cur.fetchall():
        data_dict[transaction_type]["x"].append(date)
        data_dict[transaction_type]["y"].append(amount)

    # Plot the lines for each transaction type
    for transaction_type, data in data_dict.items():
        ax.plot(data["x"], data["y"], label=transaction_type)

    # Set the axis labels and the legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title(text)
    ax.legend()

    canvas.draw()


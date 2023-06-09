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
    return cur,conn

def check_cursor(cur):
    """
    Check if a cursor is closed, and if it is, rollback the connection to restore it.
    """
    if cur.closed:
        cur.connection.rollback()

def disconnect():
    if conn:
        conn.close()
        cur.close()
        print("successfully disconnected")


def ensure_connection(cur, conn):
    if conn is None or conn.closed:
        conn = psycopg2.connect(
            host=hostname,
            database=database,
            user=uname,
            password=pwd
        )
    if cur is None or cur.closed:
        cur = conn.cursor()
    return cur, conn

def bp():
    print("button pressed")

cur, conn = connect()

def update_acc_analysis(radio,sql_exp,sql_inc,line_canvas_exp,line_ax_exp,line_canvas_inc,line_ax_inc,date_button_start,date_button_end,uid,text1,text2,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card):
    selection = radio.get()
    end_date = datetime.today()
    if selection == 0:
        start_date = end_date - timedelta(days=7)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)
        update_values_analysis(start_date, end_date, uid,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card)

    elif selection == 1:
        start_date = end_date - timedelta(days=30)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)
        update_values_analysis(start_date, end_date, uid,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card)

    elif selection == 2:
        start_date = end_date.replace(day=1)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)
        update_values_analysis(start_date, end_date, uid,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card)

    elif selection == 3:
        start_date = end_date.replace(month=1, day=1)
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)
        update_values_analysis(start_date, end_date, uid,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card)

    else:
        start_date = date_button_start.get()
        end_date = date_button_end.get()
        line_graph(sql_exp,uid,start_date,end_date,line_canvas_exp,line_ax_exp,text1)
        line_graph(sql_inc,uid,start_date,end_date,line_canvas_inc,line_ax_inc,text2)
        update_values_analysis(start_date, end_date, uid,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card)


def update_values_analysis(start_date, end_date, uid,total_expense_savings,total_income_savings,total_expense_cash,total_income_cash,total_expense_card,total_income_card):

    cur.execute(
        'select sum(amount) from expenses where id = %s and dayofexpense between %s and %s and transaction_type = %s',
        (uid, start_date, end_date, "Savings"))
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        val1 = int(row[0])
    else:
        val1 = 0
    total_expense_savings.set(val1)

    cur.execute(
        'select sum(amount) from income where id = %s and dayofincome between %s and %s and transaction_type = %s',
        (uid, start_date, end_date,"Savings"))
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        val2 = int(row[0])
    else:
        val2 = 0
    total_income_savings.set(val2)

    cur.execute(
        'select sum(amount) from expenses where id = %s and dayofexpense between %s and %s and transaction_type = %s',
        (uid, start_date, end_date,"Cash"))
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        val3 = int(row[0])
    else:
        val3 = 0
    total_expense_cash.set(val3)

    cur.execute(
        'select sum(amount) from income where id = %s and dayofincome between %s and %s and transaction_type = %s',
        (uid, start_date, end_date,"Cash"))
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        val4 = int(row[0])
    else:
        val4 = 0
    total_income_cash.set(val4)

    cur.execute(
        'select sum(amount) from expenses where id = %s and dayofexpense between %s and %s and transaction_type = %s',
        (uid, start_date, end_date,"Card"))
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        val5 = int(row[0])
    else:
        val5 = 0
    total_expense_card.set(val5)

    cur.execute(
        'select sum(amount) from income where id = %s and dayofincome between %s and %s and transaction_type = %s',
        (uid, start_date, end_date,"Card"))
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        val6 = int(row[0])
    else:
        val6 = 0
    total_income_card.set(val6)

    return total_expense_savings, total_income_savings, total_expense_cash, total_income_cash, total_expense_card, total_income_card

def check_connection(cur, conn):
    if conn.closed:
        cur, conn = connect()
    return cur, conn

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


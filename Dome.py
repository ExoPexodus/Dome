import tkinter as tk    # for GUI
from tkinter import ttk  # importing ttk libraries for tables in GUI
import tkinter.messagebox   # importing messagebox for popup messages
import customtkinter        # Custom Tkinter library for a cool Tkinter look
import custom_functions     # Custom function python script for additional database connection related functions
from tkcalendar import DateEntry    # DateEntry functions for calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   #Matplotlib for Graphs and pie chart
from matplotlib.figure import Figure     #Matplotlib for Graphs and pie chart
import matplotlib.pyplot as plt  #Matplotlib for Graphs and pie chart
from datetime import datetime, timedelta  #datetime library for time and date calculations and insertion
import Login_screen     # python script for user authentication


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# initialising a GUI using custom Tkinter
dome = customtkinter.CTk()
dome.title("Dome")
dome.geometry("1280x800")
dome.state("zoomed")

# Checking if user was successfully able to authenticate through the Login_screen script
if len(Login_screen.name) == 0:
    dome.destroy()

# if name fetched from login screen exists, fetch the uid assigned to the user for further data analysis
name = Login_screen.name
cur, conn = custom_functions.connect()
cur.execute('select id from users where name = %s',(name,))
row = cur.fetchone()
uid = int(row[0])

#Defining a default table number for table_switch and table_creation functions
table_number = 2
#=======================Defining Functions==============

def logout():
    # Logout function for logout_button
    print("button pressed")
    custom_functions.disconnect()
    if len(name) > 0:
        dome.destroy()


def insert_exp():
    # Gui popup for data insertion in the expenses table
    def enter_data_in_expenses():
        details = entry_details.get()
        amount = entry_amount.get()
        date = set_date.get()
        category = category_selection.get()
        transaction_type = transaction_type_selection.get()

        insert_script = "insert into expenses(id,details,amount,dayofexpense,category,transaction_type) values(%s,%s,%s,%s,%s,%s)"
        values = (uid, details, amount, date, category, transaction_type)
        try:
            cur.execute(insert_script, values)
            conn.commit()
            tkinter.messagebox.showinfo("Message", "Data successfully inserted")

        except Exception as e:
            conn.rollback()
            tkinter.messagebox.showerror("Error:", "Error in inserting the data: " + str(e))

    insert_expenses = customtkinter.CTk()
    insert_expenses.title("insert values")
    insert_expenses.geometry("1280x80")

    category_selection = customtkinter.CTkComboBox(insert_expenses,
                                                   values=["Housing", "Transportation", "Food",
                                                           "Personal_Care", "Health", "Entertainment","Debts_and_Loans","Miscellaneous"])
    entry_details = customtkinter.CTkEntry(insert_expenses, placeholder_text="Enter Details", width=500)
    entry_amount = customtkinter.CTkEntry(insert_expenses, placeholder_text="Enter Amount")
    set_date = DateEntry(insert_expenses, width=20, background='green', foreground='black', borderwidth=2)
    enter_data_button = customtkinter.CTkButton(insert_expenses, text="Enter Data", command=enter_data_in_expenses,
                                                width=100)
    transaction_type_selection = customtkinter.CTkComboBox(insert_expenses, values=["Cash", "Card", "Savings"])


    entry_amount.grid(row=0, column=4)
    set_date.grid(row=0, column=5)
    enter_data_button.grid(row=0, column=6)
    entry_details.grid(row=0, column=3)
    category_selection.grid(row=0, column=2, pady=20)
    transaction_type_selection.grid(row=0,columns=1)
    transaction_type_selection.set("Transaction Type")
    category_selection.set("Category")


    insert_expenses.mainloop()


def insert_inc():
    # Gui popup for data insertion in the income table
    def enter_data_in_expenses():
        details = entry_details.get()
        amount = entry_amount.get()
        date = set_date.get()
        category = category_selection.get()
        transaction_type = transaction_type_selection.get()

        insert_script = "insert into income(id,details,amount,dayofincome,source,transaction_type) values(%s,%s,%s,%s,%s,%s)"
        values = (uid, details, amount, date, category,transaction_type)

        try:
            cur.execute(insert_script, values)
            conn.commit()
            tkinter.messagebox.showinfo("Message", "Data successfully inserted")

        except Exception as e:
            conn.rollback()
            tkinter.messagebox.showerror("Error:", "Error in inserting the data: " + str(e))

    insert_expenses = customtkinter.CTk()
    insert_expenses.title("insert values")
    insert_expenses.geometry("1280x80")

    category_selection = customtkinter.CTkComboBox(insert_expenses,
                                                   values=["Salary", "Investment", "Self_Employment",
                                                           "Rental_Income", "Retirement", "Social_Security","Alimony_or_Child_Support","Miscellaneous"])
    entry_details = customtkinter.CTkEntry(insert_expenses, placeholder_text="Enter Details", width=500)
    entry_amount = customtkinter.CTkEntry(insert_expenses, placeholder_text="Enter Amount")
    set_date = DateEntry(insert_expenses, width=20, background='green', foreground='black', borderwidth=2)
    enter_data_button = customtkinter.CTkButton(insert_expenses, text="Enter Data", command=enter_data_in_expenses,
                                                width=100)
    transaction_type_selection = customtkinter.CTkComboBox(insert_expenses, values=["Cash", "Card", "Savings"])


    entry_amount.grid(row=0, column=4)
    set_date.grid(row=0, column=5)
    enter_data_button.grid(row=0, column=6)
    entry_details.grid(row=0, column=3)
    category_selection.grid(row=0, column=2, pady=20)
    transaction_type_selection.grid(row=0,columns=1)
    transaction_type_selection.set("Transaction Type")
    category_selection.set("Category")


    insert_expenses.mainloop()

def update_table_category_expense(start_date,end_date):
    # Function to update the table for categories in the expense frame
    #check if the table exists in the subdown frame and destory it if it exists
    children = dome.frame_Expenses.right.down.subdown.winfo_children()
    for child in children:
        try:
            if child == treeview_expense:
                treeview_expense.destroy()
        except NameError:
            pass
    #create a new table by calling the function below
    create_table_category_expense(start_date,end_date)

def create_table_category_expense(start_date,end_date):
    # Function to create a table for categories in the expense frame
    # create a global variable so that the table can be accessed by the functions outside of this function
    global treeview_expense
    #set up a custom style to use in the table for a better font
    custom_font = ('Arial', 18)
    style = ttk.Style()
    style.configure('Custom.Treeview', rowheight=30)
    cur.execute("SELECT distinct(category), sum(amount) FROM expenses where id = %s and dayofexpense between %s and %s group by distinct(category) order by sum(amount) desc", (uid,start_date,end_date))
    rows = cur.fetchall()

    #column names that are to be shown in the GUI
    columns = ('category', 'amount')
    treeview_expense = ttk.Treeview(dome.frame_Expenses.right.down.subdown, columns=columns, show='headings', height=6, style='Custom.Treeview')
    treeview_expense.grid(row=0, column=0, sticky='nsew')

    # Add columns to the Treeview that correspond to the columns in the retrieved data
    for col in columns:
        treeview_expense.heading(col, text=col.title())
        treeview_expense.column('category', width=350)
        treeview_expense.column('amount', width=350)

    # Insert the retrieved data as rows in the Treeview
    for row in rows:
        treeview_expense.insert('', tk.END, values=row)

    # Apply the custom font to all items in the Treeview
    treeview_expense.tag_configure('custom_font', font=custom_font)
    for row in treeview_expense.get_children():
        treeview_expense.item(row, tags=('custom_font',))


def create_table_income():
    # function to create a table for income in the GUI
    # Fetch data from the specified table
    cur.execute(f"SELECT source, details, amount, dayofincome FROM income where id = %s ORDER BY dayofincome DESC LIMIT 30",(uid,))
    rows = cur.fetchall()

    #column names that are to be shown in the GUI
    columns = ('category', 'details', 'amount', 'date')
    treeview = ttk.Treeview(dome.frame_insert.up, columns=columns, show='headings', height=20)
    treeview.grid(row=0, column=0, sticky='nsew')

    # Add columns to the Treeview that correspond to the columns in the retrieved data
    for col in columns:
        treeview.heading(col, text=col.title())
        treeview.column('category', width=500)
        treeview.column('details', width=500)
        treeview.column('amount', width=500)
        treeview.column('date', width=150)

    # Insert the retrieved data as rows in the Treeview
    for row in rows:
        treeview.insert('', tk.END, values=row)

def create_table_expense():
    # function to create a table for expenses in the GUI
    cur.execute(
        "SELECT category,details,amount,dayofexpense FROM expenses where id = %s order by dayofexpense desc limit 30",
        (uid,))
    rows = cur.fetchall()

    #column names that are to be shown in the GUI
    columns = ('category', 'details', 'amount', 'date')
    treeview = ttk.Treeview(dome.frame_insert.up, columns=columns, show='headings', height=20)
    treeview.grid(row=0, column=0, sticky='nsew')

    # Add columns to the Treeview that correspond to the columns in the retrieved data
    for col in columns:
        treeview.heading(col, text=col.title())
        treeview.column('category', width=500)
        treeview.column('details', width=500)
        treeview.column('amount', width=500)
        treeview.column('date', width=150)

    # Insert the retrieved data as rows in the Treeview
    for row in rows:
        treeview.insert('', tk.END, values=row)
def switch_table_expense():
    # function to switch to expenses table
    #look for all the tables in the specified frame and
    #delete the tables if found with the same variable names as specified below

    children = dome.frame_insert.up.winfo_children()
    for child in children:
        try:
            if child == treeview1:
                treeview1.destroy()
        except NameError:
            pass
        try:
            if child == treeview2:
                treeview2.destroy()
        except NameError:
            pass
        try:
            if child == treeview:
                treeview.destroy()
        except NameError:
            pass

    #create a new expense table as a replacement to the old one
    create_table_expense()

def switch_table_income():
    # function to switch to income table
    #look for all the tables in the specified frame and
    #delete the tables if found with the same variable names as specified below
    children = dome.frame_insert.up.winfo_children()
    for child in children:
        try:
            if child == treeview1:
                treeview1.destroy()
        except NameError:
            pass
        try:
            if child == treeview2:
                treeview2.destroy()
        except NameError:
            pass
        try:
            if child == treeview:
                treeview.destroy()
        except NameError:
            pass

    #create a new expense table as a replacement to the old one
    create_table_income()


def create_double_table():
    #function to create two different tables for both expenses and income
    #destory any pre-made tables after looking for them with wininfo_childeren()
    children = dome.frame_insert.up.winfo_children()
    for child in children:
        if child == treeview:
            child.destroy()
    # Fetch data for the first table
    cur.execute("SELECT category, details, amount, dayofexpense FROM expenses where id = %s order by dayofexpense desc limit 30",(uid,))
    rows1 = cur.fetchall()

    # Fetch data for the second table
    cur.execute("SELECT source, details, amount, dayofincome FROM income where id = %s ORDER BY dayofincome DESC LIMIT 30",(uid,))
    rows2 = cur.fetchall()

    columns = ('Category', 'Details', 'Amount', 'Date')

    # Create the first Treeview widget
    global treeview1
    treeview1 = ttk.Treeview(dome.frame_insert.up, columns=columns, show='headings', height=20)
    treeview1.grid(row=0, column=0, sticky='nsew')

    # Configure the column width for the first Treeview widget
    column_widths1 = {'Category': 200, 'Details': 200, 'Amount': 200, 'Date': 200}
    for col, width in column_widths1.items():
        treeview1.heading(col, text=col.title())
        treeview1.column(col, width=width)

    # Insert the retrieved data as rows in the first Treeview
    for row in rows1:
        treeview1.insert('', tk.END, values=row)

    # Create the second Treeview widget
    global treeview2
    treeview2 = ttk.Treeview(dome.frame_insert.up, columns=columns, show='headings', height=20)
    treeview2.grid(row=0, column=1, sticky='nsew')

    # Configure the column width for the second Treeview widget
    column_widths2 = {'Category': 200, 'Details': 200, 'Amount': 200, 'Date': 200}
    for col, width in column_widths2.items():
        treeview2.heading(col, text=col.title())
        treeview2.column(col, width=width)

    # Insert the retrieved data as rows in the second Treeview
    for row in rows2:
        treeview2.insert('', tk.END, values=row)

def switch_table_income_delete():
    # Fetch data from the specified table
    cur.execute(f"SELECT source, details, amount, dayofincome,transactionid FROM income where id = %s ORDER BY dayofincome DESC LIMIT 30",(uid,))
    rows = cur.fetchall()

    # Get the current number of rows in the Treeview
    num_rows = len(treeview_delete.get_children())

    # Remove any existing rows from the Treeview
    if num_rows > 0:
        treeview_delete.delete(*treeview_delete.get_children())

    # Insert the retrieved data as rows in the Treeview
    for row in rows:
        treeview_delete.insert('', tk.END, values=row)

    global table_number
    table_number = 1

def switch_table_expense_delete():

    cur.execute(
        "SELECT category,details,amount,dayofexpense, transactionid FROM expenses where id = %s order by dayofexpense desc limit 30",
        (uid,))
    rows = cur.fetchall()

    # Get the current number of rows in the Treeview
    num_rows = len(treeview_delete.get_children())

    # Remove any existing rows from the Treeview
    if num_rows > 0:
        treeview_delete.delete(*treeview_delete.get_children())

    # Insert the retrieved data as rows in the Treeview
    for row in rows:
        treeview_delete.insert('', tk.END, values=row)

    global table_number
    table_number = 2


def make_changes():

    color = combobox_color.get()
    appearance = combobox_apperance.get()

    customtkinter.set_default_color_theme(color)
    customtkinter.set_appearance_mode(appearance)
    dome.state("zoomed")


def show_frame(frame):
    frame.tkraise()

def fetch_expenses_data(start_date, end_date):
    cur.execute("SELECT distinct(category) as category, SUM(amount) FROM expenses WHERE dayofexpense >= %s AND dayofexpense <= %s AND id = %s GROUP BY category", (start_date, end_date,uid))
    rows = cur.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = row[1]
    return data

# function to calculate percentage for each category
def calculate_percentage(data):
    total = sum(data.values())
    percentages = {}
    for category, amount in data.items():
        percentages[category] = amount/total * 100
    return percentages

def update_pie_chart(start_date, end_date):
    data = fetch_expenses_data(start_date, end_date)
    percentages = calculate_percentage(data)
    labels = percentages.keys()
    sizes = percentages.values()
    pie_ax.clear() # clear previous chart
    pie_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    pie_ax.set_title(f"Expenses by Category ({start_date} to {end_date})")
    canvas.draw()


def update_bar_graph(start_date,end_date):
    # Clear the current bar graph
    barax.clear()

    # Fetch data from the database
    cur.execute('select distinct category,sum(amount) as amount from expenses where dayofexpense between %s and %s and id = %s group by category order by amount;',(start_date,end_date,uid))

    data = cur.fetchall()
    print(data)

    values = {}

    for category, value in data:
        # Limit the category name to 10 characters using string slicing

        max_key_len = category.find("_")
        if max_key_len >= 0:
            category_name = category[:max_key_len]
        else:
            category_name = category
        # Alternatively, limit the category name to 10 characters using the truncate() method
        # category_name = category[:10].truncate(10)

        if category_name not in values:
            values[category_name] = value
        else:
            values[category_name] += value
    barax.bar(values.keys(), values.values())
    barax.set_xlabel('Category')
    barax.set_ylabel('Value')
    barax.set_title('Expenses')


    bar_canvas.draw()

def update_values(start_date,end_date):
    global total_expense
    global total_income
    global total_savings
    cur.execute('select sum(amount) from expenses where id = %s and dayofexpense between %s and %s', (uid,start_date,end_date))
    row = cur.fetchone()
    val1 = int(row[0])
    total_expense.set(val1)

    cur.execute('select sum(amount) from income where id = %s and dayofincome between %s and %s', (uid,start_date,end_date))
    row1 = cur.fetchone()
    val2 = int(row1[0])
    total_income.set(val2)

    val3 = val2 - val1
    total_savings.set(val3)
    return total_savings,total_expense,total_income

def update_expenses():
    selection = radio_var.get()
    end_date = datetime.today()
    if selection == 0:
        start_date = end_date - timedelta(days=7)
        update_pie_chart(start_date,end_date)
        update_bar_graph(start_date,end_date)
        update_values(start_date, end_date)
        update_table_category_expense(start_date,end_date)
    elif selection == 1:
        start_date = end_date - timedelta(days=30)
        update_pie_chart(start_date,end_date)
        update_bar_graph(start_date,end_date)
        update_values(start_date, end_date)
        update_table_category_expense(start_date,end_date)
    elif selection == 2:
        start_date = end_date.replace(day=1)
        update_pie_chart(start_date,end_date)
        update_bar_graph(start_date,end_date)
        update_values(start_date, end_date)
        update_table_category_expense(start_date,end_date)
    elif selection == 3:
        start_date = end_date.replace(month=1, day=1)
        update_pie_chart(start_date,end_date)
        update_bar_graph(start_date,end_date)
        update_values(start_date, end_date)
        update_table_category_expense(start_date,end_date)
    else:
        start_date = custom_radio_button_start.get()
        end_date = custom_radio_button_end.get()
        update_pie_chart(start_date,end_date)
        update_bar_graph(start_date,end_date)
        update_values(start_date, end_date)
        update_table_category_expense(start_date,end_date)
def delete_selection():
    # Get the selected row
    selection = treeview_delete.selection()

    # If a row is selected, get the ID of the selected row
    if selection:
        row = treeview_delete.item(selection[0])['values']
        row_id = row[4]  # Assuming the ID is the first column

        try:

            # Build the SQL query to delete the row from the table
            if table_number == 1:
                sql = f"DELETE FROM income WHERE transactionid = {row_id}"
                cur.execute(sql)
                conn.commit()

            elif table_number == 2:
                sql = f"DELETE FROM expenses WHERE transactionid = {row_id}"
                cur.execute(sql)
                conn.commit()

            # Delete the selected row from the Treeview
            treeview_delete.delete(selection[0])
            # Notify the user that the row has been deleted
            tkinter.messagebox.showinfo("Success", f"Row {row_id} has been deleted from expenses table.")

        except Exception as e:
            # If there is an error, rollback the changes and show an error message
            conn.rollback()
            tkinter.messagebox.showerror("Error", str(e))

    # If no row is selected, show a message to the user
    else:
        tkinter.messagebox.showerror("Error", "Please select a row to delete.")

#========================decleration for the first 2 frames===============================

dome.grid_columnconfigure(1, weight=1)
dome.grid_rowconfigure(0, weight=1)

dome.frame_left = customtkinter.CTkFrame(master=dome,
                                         width=180,
                                         corner_radius=0)
dome.frame_left.grid(row=0, column=0, sticky="nswe")

dome.frame_acc_analysis = customtkinter.CTkFrame(master=dome)
dome.frame_Income = customtkinter.CTkFrame(master=dome)
dome.frame_Expenses = customtkinter.CTkFrame(master=dome)
dome.frame_insert = customtkinter.CTkFrame(master=dome)
dome.frame_delete = customtkinter.CTkFrame(master=dome)
dome.frame_settings = customtkinter.CTkFrame(master=dome)

for frame in (dome.frame_delete,dome.frame_insert,dome.frame_settings,dome.frame_Expenses,dome.frame_Income,dome.frame_acc_analysis):
    frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

dome.frame_Expenses.left = customtkinter.CTkFrame(master=dome.frame_Expenses)
dome.frame_Expenses.right = customtkinter.CTkFrame(master=dome.frame_Expenses)
dome.frame_Expenses.right.up = customtkinter.CTkFrame(master=dome.frame_Expenses.right)
dome.frame_Expenses.right.down = customtkinter.CTkFrame(master=dome.frame_Expenses.right)
dome.frame_Expenses.right.down.subup = customtkinter.CTkFrame(master=dome.frame_Expenses.right.down)
dome.frame_Expenses.right.down.subdown = customtkinter.CTkFrame(master=dome.frame_Expenses.right.down)
dome.frame_Expenses.right.up.grid(row=0,column=0,sticky="nswe",padx=20,pady=20)
dome.frame_Expenses.right.down.grid(row=1,column=0,sticky="nswe",padx=20,pady=20)
dome.frame_Expenses.right.down.subup.grid(row=0,column=0,sticky="nswe",padx=20,pady=20)
dome.frame_Expenses.right.down.subdown.grid(row=1,column=0,sticky="nswe",padx=20,pady=20)
dome.frame_Expenses.right.grid(row=0,column=1,sticky="nswe",padx=20,pady=20)
dome.frame_Expenses.left.grid(row=0,column=0,sticky="nswe",padx=20,pady=20)

dome.frame_insert.up = customtkinter.CTkFrame(master=dome.frame_insert)
dome.frame_insert.down = customtkinter.CTkFrame(master=dome.frame_insert)
dome.frame_insert.up.grid(row=0,column=0,padx=20,pady=20)
dome.frame_insert.down.grid(row=1,column=0,padx=20,pady=20)

dome.frame_delete.up = customtkinter.CTkFrame(master=dome.frame_delete)
dome.frame_delete.down = customtkinter.CTkFrame(master=dome.frame_delete)
dome.frame_delete.up.grid(row=0,column=0,padx=20,pady=20)
dome.frame_delete.down.grid(row=1,column=0,padx=20,pady=20)

#===========================Left frame=========================
dome.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
dome.frame_left.grid_rowconfigure(5, weight=1)   # empty row as spacing
dome.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
dome.frame_left.grid_rowconfigure(11, minsize=10)

# Configure the first three columns to have a minimum size of 100 pixels
# and to not expand when the window is resized
for i in range(3):
    dome.frame_insert.down.grid_columnconfigure(i, minsize=100, weight=0)

# Configure the next two columns to expand when the window is resized
for i in range(3, 5):
    dome.frame_insert.down.grid_columnconfigure(i, minsize=200 ,weight=1)

# Configure the next two columns to have a minimum size of 20 pixels
# and to not expand when the window is resized
for i in range(5, 7):
    dome.frame_insert.down.grid_columnconfigure(i, minsize=20, weight=0)

# Configure the last two columns to have a minimum size of 100 pixels
# and to not expand when the window is resized
for i in range(7, 9):
    dome.frame_insert.down.grid_columnconfigure(i, minsize=100, weight=0)

for i in range(3):
    dome.frame_delete.down.grid_columnconfigure(i, minsize=100, weight=0)

# Configure the next two columns to expand when the window is resized
for i in range(3, 5):
    dome.frame_delete.down.grid_columnconfigure(i, minsize=200 ,weight=1)

# Configure the next two columns to have a minimum size of 20 pixels
# and to not expand when the window is resized
for i in range(5, 7):
    dome.frame_delete.down.grid_columnconfigure(i, minsize=20, weight=0)

# Configure the last two columns to have a minimum size of 100 pixels
# and to not expand when the window is resized
for i in range(7, 9):
    dome.frame_delete.down.grid_columnconfigure(i, minsize=100, weight=0)

user_label = customtkinter.CTkLabel(master=dome.frame_left,text = name)
user_label.grid(row=1, column=0, pady=10, padx=10)

account_analysis_button = customtkinter.CTkButton(dome.frame_left,text = "Account_Analysis",command=lambda:show_frame(dome.frame_acc_analysis))
account_analysis_button.grid(row=2, column=0, pady=10, padx=10)

expenses_button = customtkinter.CTkButton(dome.frame_left,text = "Expenses",command=lambda:show_frame(dome.frame_Expenses))
expenses_button.grid(row=3, column=0, pady=10, padx=10)

income_button = customtkinter.CTkButton(dome.frame_left,text = "Income",command=lambda:show_frame(dome.frame_Income))
income_button.grid(row=4, column=0, pady=10, padx=10)

insert_button = customtkinter.CTkButton(dome.frame_left,text = "Insert",command=lambda:show_frame(dome.frame_insert))
insert_button.grid(row=5, column=0, pady=10, padx=10)

edit_button = customtkinter.CTkButton(dome.frame_left,text = "Delete",command=lambda:show_frame(dome.frame_delete))
edit_button.grid(row=6, column=0, pady=10, padx=10)

Settings_button = customtkinter.CTkButton(dome.frame_left,text = "Settings",command=lambda:show_frame(dome.frame_settings))
Settings_button.grid(row=9, column=0, pady=10, padx=10)

Logout_button = customtkinter.CTkButton(dome.frame_left, text = "Logout",command=logout)
Logout_button.grid(row=10,column=0,pady=10,padx=10)

#============================Expenses Frame===============================

total_expense = tk.StringVar()
total_income = tk.StringVar()
total_savings = tk.StringVar()

end_date = datetime.today()
start_date = end_date - timedelta(days=7)
update_values(start_date, end_date)

barfig = Figure(figsize=(8, 4), dpi=100)
barax = barfig.add_subplot()
bar_canvas = FigureCanvasTkAgg(barfig, master=dome.frame_Expenses.left)
bar_canvas.get_tk_widget().grid(row=1, column=0)
barfig.suptitle('Expenses for the specified time period')

fig = plt.Figure(figsize=(8,5), dpi=100)
pie_ax = fig.add_subplot(111)
pie_ax.set_title("Expenses by Category")
pie_ax.axis('equal')
canvas = FigureCanvasTkAgg(fig, master=dome.frame_Expenses.left)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0)

radio_var = tkinter.IntVar(value=0)
week_radio_button = customtkinter.CTkRadioButton(master=dome.frame_Expenses.right.up,
                                                           variable=radio_var,
                                                           value=0,text="Show data for the last 7 days",command=update_expenses)
month_radio_button = customtkinter.CTkRadioButton(master=dome.frame_Expenses.right.up,
                                                           variable=radio_var,
                                                           value=1,text="Show data for the last 30 days",command=update_expenses)
half_year_radio_button = customtkinter.CTkRadioButton(master=dome.frame_Expenses.right.up,
                                                           variable=radio_var,
                                                           value=2,text="Show data for This month",command=update_expenses)
year_radio_button = customtkinter.CTkRadioButton(master=dome.frame_Expenses.right.up,
                                                           variable=radio_var,
                                                           value=3,text = "Show data for this Year",command=update_expenses)
custom_time_period_radio_button = customtkinter.CTkRadioButton(master=dome.frame_Expenses.right.up,
                                                               variable=radio_var,value=4,text="Show data based on the dates specified below",command=update_expenses)
custom_radio_button_start = DateEntry(dome.frame_Expenses.right.up, width=40, background='blue', foreground='white', borderwidth=2)
custom_radio_button_end = DateEntry(dome.frame_Expenses.right.up, width=40, background='blue', foreground='white', borderwidth=2)
label_from = customtkinter.CTkLabel(dome.frame_Expenses.right.up,text="Date starting from")
label_to = customtkinter.CTkLabel(dome.frame_Expenses.right.up,text ="Date ending at")


custom_time_period_radio_button.grid(row=4,column=0,padx=20,pady=20)
custom_radio_button_start.grid(row=6,column=0,padx=40,pady=20)
custom_radio_button_end.grid(row=6,column=1,padx=40,pady=20)
week_radio_button.grid(row=0,column=0,pady=20)
month_radio_button.grid(row=1,column=0,pady=20)
half_year_radio_button.grid(row=2,column=0,pady=20)
year_radio_button.grid(row=3,column=0,pady=20)
label_to.grid(row=5,column=1,padx=40,pady=20)
label_from.grid(row=5,column=0,padx=40,pady=20)

label_total_expenses = customtkinter.CTkLabel(dome.frame_Expenses.right.down.subup,width=40,text_font=("Arial", 14, "bold"), text="Total Expenses: ")
label_total_income = customtkinter.CTkLabel(dome.frame_Expenses.right.down.subup,width=40,text_font=("Arial", 14, "bold"), text="Total Income: ")
label_total_savings = customtkinter.CTkLabel(dome.frame_Expenses.right.down.subup,width=40,text_font=("Arial", 14, "bold"), text="Total Savings: ")

label_total_expenses_value = customtkinter.CTkLabel(dome.frame_Expenses.right.down.subup,width=40,text_font=("Arial", 14, "bold"),textvariable=total_expense)
label_total_income_value = customtkinter.CTkLabel(dome.frame_Expenses.right.down.subup,width=40,text_font=("Arial", 14, "bold"),textvariable=total_income)
label_total_savings_value = customtkinter.CTkLabel(dome.frame_Expenses.right.down.subup,width=40,text_font=("Arial", 14, "bold"),textvariable=total_savings)

label_total_expenses.grid(row=1,column=0,pady=20)
label_total_income.grid(row=1,column=2,padx=(20,0),pady=20)
label_total_savings.grid(row=1,column=4,padx=(20,0),pady=20)
label_total_expenses_value.grid(row=1,column=1,pady=20)
label_total_income_value.grid(row=1,column=3,pady=20)
label_total_savings_value.grid(row=1,column=5,pady=20)

create_table_category_expense(start_date,end_date)
#============================Insert Frames==========================


cur.execute("SELECT category,details,amount,dayofexpense FROM expenses where id = %s order by dayofexpense desc limit 30",(uid,))
rows = cur.fetchall()

columns = ('category', 'details','amount','date')  # replace with the actual column names
treeview = ttk.Treeview(dome.frame_insert.up, columns=columns, show='headings',height=20)
treeview.grid(row=0, column=0, sticky='nsew')

# Add columns to the Treeview that correspond to the columns in the retrieved data
for col in columns:
    treeview.heading(col, text=col.title())
    treeview.column('category',width=500)
    treeview.column('details',width=500)
    treeview.column('amount',width=500)
    treeview.column('date',width=150)

# Insert the retrieved data as rows in the Treeview
for row in rows:
    treeview.insert('', tk.END, values=row)


view_expenses_table_button = customtkinter.CTkButton(dome.frame_insert.down,text='Expenses Table',command=switch_table_expense)
view_income_table_button = customtkinter.CTkButton(dome.frame_insert.down,text='Income Table',command=switch_table_income)
view_Both_table_button = customtkinter.CTkButton(dome.frame_insert.down,text='Split Table', command=create_double_table )
insert_expenses_button = customtkinter.CTkButton(dome.frame_insert.down,text='Insert Expenses',command=insert_exp)
insert_income_button = customtkinter.CTkButton(dome.frame_insert.down,text='Insert Income',command=insert_inc)

view_expenses_table_button.grid(row=0,column=0, sticky='w')
view_income_table_button.grid(row=0,column=1, sticky='w', padx=10)
view_Both_table_button.grid(row=0,column=2, sticky='w')
insert_expenses_button.grid(row=0,column=7, sticky='e', padx=10)
insert_income_button.grid(row=0,column=8, sticky='e')

#=======================Delete frame===============================

cur.execute("SELECT category,details,amount,dayofexpense,transactionid FROM expenses where id = %s order by dayofexpense desc limit 30",(uid,))
rows = cur.fetchall()

columns = ('category', 'details','amount','date','id')  # replace with the actual column names
treeview_delete = ttk.Treeview(dome.frame_delete.up, columns=columns, show='headings',height=20)
treeview_delete.grid(row=0, column=0, sticky='nsew')

# Add columns to the Treeview that correspond to the columns in the retrieved data
for col in columns:
    treeview_delete.heading(col, text=col.title())
    treeview_delete.column('category',width=500)
    treeview_delete.column('details',width=500)
    treeview_delete.column('amount',width=500)
    treeview_delete.column('date',width=150)

# Insert the retrieved data as rows in the Treeview
for row in rows:
    treeview_delete.insert('', tk.END, values=row)

view_expenses_table_button_delete = customtkinter.CTkButton(dome.frame_delete.down,text='Expenses Table',command=switch_table_expense_delete)
view_income_table_button_delete = customtkinter.CTkButton(dome.frame_delete.down,text='Income Table',command=switch_table_income_delete)
delete_row_button = customtkinter.CTkButton(dome.frame_delete.down,text='Delete Row', command=delete_selection)

view_expenses_table_button_delete.grid(row=0,column=0, sticky='w')
view_income_table_button_delete.grid(row=0,column=1, sticky='w', padx=10)
delete_row_button.grid(row=0,column=8, sticky='e')


#===========================settings frame======================

fourth_label = customtkinter.CTkLabel(dome.frame_settings, text="Modes & Theme")
fourth_label.grid(row=1,column=1)

combobox_apperance = customtkinter.CTkComboBox(master=dome.frame_settings,
                                                values=["Dark","Light"])

combobox_apperance.grid(row=2, column=1, pady=10, padx=20, sticky="w")

combobox_color = customtkinter.CTkComboBox(master=dome.frame_settings,
                                                values=["green", "dark-blue", "blue"])


combobox_color.grid(row=2, column=2, pady=10, padx=20, sticky="w")
confirm_button = customtkinter.CTkButton(master=dome.frame_settings,text="Apply Changes",command=make_changes)
confirm_button.grid(row=2, column=3, pady=10, padx=20, sticky="w")

#===========================Default Values======================


week_radio_button.select()


selection = radio_var.get()
end_date = datetime.today()
start_date = end_date - timedelta(days=7)
update_pie_chart(start_date, end_date)
update_bar_graph(start_date, end_date)
show_frame(dome.frame_Expenses)
custom_functions.disconnect()


dome.mainloop()



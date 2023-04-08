import tkinter.messagebox   # For the default errors and message popups
import customtkinter     # Custom Tkinter library for a cool Tkinter look
import custom_functions     # Custom function python script for additional database connection related functions

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

#=============Global Variables===============
username = None
email = None
password = None
confirm_password = None
#=========================DB Variables=====================
cur, conn = custom_functions.connect()
#========================Function Decleration=========================

# function to switch to register frame
def register():
    print("Account creation screen opened")
    login.pack_forget()
    reg.pack()
#function to switch to welcome screen showing the username of the user
def welcome():
    app.destroy()
    welcome_screen = customtkinter.CTk()
    welcome_screen.title("Dome")
    welcome_screen.geometry("300x200")

    welcome_label = customtkinter.CTkLabel(welcome_screen, text = "Welcome "+name)
    welcome_label.pack(pady=5)
    welcome_screen.after(10,welcome_screen.destroy())
    welcome_screen.mainloop()

#function to go back to the login screen
def back():
    print("Going back to login screen")
    reg.pack_forget()
    login.pack()

def authentication():
    global name
    name = name_entry.get()
    global password
    password = password_entry.get()
    global uid


    selectscript = "Select * from users where name = '%s' and pass = '%s'"%(name,password)
    cur.execute(selectscript)
    if len(name) == 0:
        tkinter.messagebox.showerror("Error", "please fill the username field")
    elif len(password) == 0:
        tkinter.messagebox.showerror("Error","please fill the password field")
    elif cur.fetchall():
        print("Account Authincated")
        welcome()
    else:
        print("Credentials don't exist")
        tkinter.messagebox.showerror("Error","Error: The credentials do not match with the database")


def account_creation():

        username = username_entry.get()
        email = email_entry1.get()
        password = password_entry1.get()
        confirm_password = confirm_password_entry.get()

        check_user_script = "select * from users where name = '%s'"%(username)
        check_email_script = "select * from users where email = '%s'"%(email)
        if len(username) == 0:
            tkinter.messagebox.showerror("Error", "Error: username is empty")
        else:
            cur.execute(check_user_script)
            if cur.fetchall():
                tkinter.messagebox.showerror("Error", "Error: username already exists")
            elif len(email) == 0:
                    tkinter.messagebox.showerror("Error", "Error: Email is empty")
            elif '@' not in email or not email.index('@') > 0 and email.index('@') < len(email) - 5:
                    tkinter.messagebox.showerror("Error","Error: Email written incorrectly, please make sure you're writing the email correctly")
            elif not email.endswith('.com'):
                    tkinter.messagebox.showerror("Error","Error: Email written incorrectly, please make sure you're writing the email correctly")
            else:
                cur.execute(check_email_script)
                if cur.fetchall():
                    tkinter.messagebox.showerror("Error", "Error: email already exists")
                elif len(password) <= 7:
                    tkinter.messagebox.showerror("Error", "Error: Please make the password at least 8 characters for security reasons")
                elif password == confirm_password:

                    insertscript = "insert into users(name,email,pass) values('%s','%s','%s')"%(username,email,password)
                    cur.execute(insertscript)
                    conn.commit()
                    print("account created")
                    tkinter.messagebox.showinfo("Message", "Account Successfully Created")
                    back()
                else:
                    print("The passwords do not match")
                    tkinter.messagebox.showerror("Error", "Passwords do not match")

def on_enter_press(event):
    # simulate a button click using enter key
    authentication()


class AuthenticationGUI:
    def __init__(self):
#=======================initialising the GUI====================
        self.app = customtkinter.CTk()
        self.app.title("Dome")
        self.app.geometry("450x200")
#=============================Login Frame==================================
        self.login = customtkinter.CTkFrame(app)
        self.button_log = customtkinter.CTkButton(login, text="Login", command=authentication)
        self.button_log.grid(column=0,row=3,sticky= "s")
        self.button_reg = customtkinter.CTkButton(login, text="Register", command=register)
        self.button_reg.grid(column=1,row=3,sticky= "s")

        self.label_email = customtkinter.CTkLabel(master=login,text = "Username")
        self.label_email.grid(row = 0,column = 0)
        self.label_pass = customtkinter.CTkLabel(master=login,text= "Password")
        self.label_pass.grid(row=1,column = 0)

        self.name_entry = customtkinter.CTkEntry(master=login,placeholder_text="Enter your username")
        self.name_entry.grid(row=0, column=1,columnspan=2)
        self.password_entry = customtkinter.CTkEntry(master=login,placeholder_text="Enter your password")
        self.password_entry.grid(row=1, column=1,columnspan=2)

#============================Register Frame=================================

        self.reg = customtkinter.CTkFrame(app)

        self.username_entry = customtkinter.CTkEntry(master=reg,placeholder_text="Enter your Username")
        self.username_entry.grid(row=0, column=1,columnspan=2)
        self.email_entry1 = customtkinter.CTkEntry(master=reg,placeholder_text="Enter your Email")
        self.email_entry1.grid(row=1, column=1,columnspan=2)
        self.password_entry1 = customtkinter.CTkEntry(master=reg,placeholder_text="Enter your Password")
        self.password_entry1.grid(row=2, column=1,columnspan=2)
        self.confirm_password_entry = customtkinter.CTkEntry(master=reg,placeholder_text="Retype your Password")
        self.confirm_password_entry.grid(row=3, column=1,columnspan=2)



        self.label_username = customtkinter.CTkLabel(master=reg,text = "Username")
        self.label_username.grid(row = 0,column = 0)
        self.label_email1 = customtkinter.CTkLabel(master=reg,text = "Email")
        self.label_email1.grid(row = 1,column = 0)
        self.label_pass1 = customtkinter.CTkLabel(master=reg,text= "Password")
        self.label_pass1.grid(row=2,column = 0)
        self.label_confirm_pass = customtkinter.CTkLabel(master=reg,text= "Confirm Password")
        self.label_confirm_pass.grid(row=3,column = 0)


        self.button_create_acc = customtkinter.CTkButton(reg, text="Create Account", command=account_creation)
        self.button_create_acc.grid(column=1,row=5,sticky= "s")
        self.button_back = customtkinter.CTkButton(reg, text="Go back", command=back)
        self.button_back.grid(column=2,row=5,sticky= "s")

        self.app.bind('<Return>', on_enter_press)
        self.login.pack()

app.mainloop()

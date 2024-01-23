from tkinter import *
from tkinter import messagebox

# wapp to insert data into student table ---> create
from sqlite3 import *
con = None






# Function to handle the sign-in logic
def signup():
    try:
        con = connect("createacc.db")
        cursor = con.cursor()
        sql = "insert into signup values('%s', '%s', %s, %s)"
        email = input("Enter the email ")
        username = input("Enter the username ")
        create_password = input("Enter the password")
        confirm_password = input("Confirm the password")
        cursor.execute(sql % (email, username, create_password, confirm_password))
        con.commit()
        print("record created")


    except Exception as e:
        con.rollback()
        print("issue is ", e)

    finally:
        if con is not None:
            con.close()
    username = usern.get()
    create_password = cpwd.get()
    confirm_password = ccpwd.get()
    email = mail.get()

    if email == "" or email == 'Enter Email':
        messagebox.showerror("ERROR FOUND", "Invalid! Enter Email ID")
    elif username == '' or username == 'Create Username':
        messagebox.showerror("ERROR FOUND", "Invalid! Enter Username")
    elif create_password == '' or create_password == 'Create Password':
        messagebox.showerror("ERROR FOUND", "Invalid! Fill in Create password")
    elif confirm_password == '' or confirm_password == 'Confirm Password':
        messagebox.showerror("ERROR FOUND", "Invalid! Fill in confirm password")
    elif create_password != confirm_password:
        messagebox.showerror("ERROR FOUND", "Invalid! Created password does not match with confirm password")

def on_enter_mail(e):
    mail.delete(0, 'end')
def on_leave_mail(e):
    email = mail.get()
    if email == '':
        mail.insert(0, 'Enter Email')
def on_enter(e):
    usern.delete(0, 'end')
def on_leave(e):
    name = usern.get()
    if name == '':
        usern.insert(0, 'Create Username')
def on_enter_cpwd(e):
    cpwd.delete(0, 'end')
    cpwd.config(show='*')
def on_leave_cpwd(e):
    create_password = cpwd.get()
    if create_password == '':
        cpwd.delete(0, 'end')
        cpwd.config(show='')
        cpwd.insert(0, ' Create Password')
def on_enter_ccpwd(e):
    ccpwd.delete(0, 'end')
    ccpwd.config(show='*')
def on_leave_ccpwd(e):
    confirm_password = ccpwd.get()
    if confirm_password == '':
        ccpwd.delete(0, 'end')
        ccpwd.config(show='')
        ccpwd.insert(0, 'Confirm Password')

# Create the main window
window = Tk()
window.title('Login')
window.geometry('1570x780')
window.configure(bg='#aec8e6')

# Load background image
img = PhotoImage(file='bg1.png')
Label(window, image=img, height=600, width=550).place(x=180, y=85)

# Create a frame for the sign-up form
frame = Frame(window, height=605, width=600, bg='white')
frame.place(x=725, y=85)

# Heading for the sign-up form
heading = Label(frame, pady=35, padx=20, text='Sign up', fg='#00008b', bg='white',
                font=('Microsoft YaHei UI Light', 28, 'bold'))
heading.place(x=200, y=5)


# Entry for email
mail = Entry(frame, width=33, fg='black', bg='white', font=('Microsoft YaHei UI Light', 15))
mail.place(x=60, y=150)
mail.insert(0, 'Enter Email')
mail.bind('<FocusIn>', on_enter_mail)
mail.bind('<FocusOut>', on_leave_mail)
Frame(frame, width=390, height=2, bg='#00008b').place(x=55, y=190)

# Entry for username
usern = Entry(frame, width=33, fg='black', bg='white', font=('Microsoft YaHei UI Light', 15))
usern.place(x=60, y=230)
usern.insert(0, 'Create Username')
usern.bind('<FocusIn>', on_enter)
usern.bind('<FocusOut>', on_leave)
Frame(frame, width=390, height=2, bg='#00008b').place(x=55, y=270)

# Entry for creating password

cpwd = Entry(frame, width=33, fg='black', bg='white', font=('Microsoft YaHei UI Light', 15))
cpwd.place(x=60, y=310)
cpwd.insert(0, ' Create Password')
cpwd.bind('<FocusIn>', on_enter_cpwd)
cpwd.bind('<FocusOut>', on_leave_cpwd)
Frame(frame, width=390, height=2, bg='#00008b').place(x=55, y=350)

# Entry for confirming password


ccpwd = Entry(frame, width=33, fg='black', bg='white', font=('Microsoft YaHei UI Light', 15))
ccpwd.place(x=60, y=390)
ccpwd.insert(0, 'Confirm Password')
ccpwd.bind('<FocusIn>', on_enter_ccpwd)
ccpwd.bind('<FocusOut>', on_leave_ccpwd)
Frame(frame, width=390, height=2, bg='#00008b').place(x=55, y=430)

# Button for sign-up
sign_up = Button(frame, width=35, pady=7, text='Sign up', bg='#3030f8', fg='white', border=0, font='20',command=signup).place(x=50, y=480)

# Label for sign-in link
label = Label(frame, text='Already have an account?', font=('Microsoft YaHei UI Light', 11), bg='white')
label.place(x=80, y=530)

# Sign-in link button
sign_in = Button(frame, text='Sign-in', border=0, bg='white', fg='#3030f8', font=('Microsoft YaHei UI Light', 12),)
sign_in.place(x=260, y=528)

# Start the main loop
window.mainloop()

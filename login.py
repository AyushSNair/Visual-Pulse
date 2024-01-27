from tkinter import *
from tkinter import messagebox
import sqlite3
import bcrypt


def signup():
    window.destroy()
    import signup

def signin():

    username = user.get()
    entered_password = pwd.get()

    if username == '' or entered_password == '':
        messagebox.showerror("Error", "All Fields Are Required")
        return

    conn = sqlite3.connect("signupdb")
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT create_password FROM signup WHERE username=? AND create_password=?',
                       [user.get(), pwd.get()])

        result_password = cursor.fetchone()

        if result_password:
            hashed_password = result_password[0].encode('UTF-8')
            entered_password_encoded = entered_password.encode('UTF-8')

            try:
                if bcrypt.checkpw(entered_password_encoded, hashed_password):
                    messagebox.showinfo("Success", "Login Successful!")
                else:
                    messagebox.showerror("Error", "Invalid Password")
            except ValueError as e:
                # If there is a ValueError, it may be due to an invalid salt
                # Regenerate salt and check again
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(entered_password_encoded, salt)

                if bcrypt.checkpw(entered_password_encoded, hashed_password):
                    messagebox.showinfo("Success", "Login Successful!")
                else:
                    messagebox.showerror("Error", "Invalid Password")
        else:
            messagebox.showerror("Error", "Invalid Username or password")


def on_enter(e):
    user.delete(0, 'end')
def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

def on_enter_password(e):
    pwd.delete(0, 'end')
    pwd.config(show='*')
def on_leave_password(e):
    entered_password = pwd.get()
    if entered_password == '':
        pwd.delete(0, 'end')
        pwd.config(show='')
        pwd.insert(0, 'Password')


# Create the main window
window = Tk()
window.title('Login')
window.geometry('1570x780')
window.configure(bg='#adc8e6')


# Load background image
img = PhotoImage(file='bg2.png')
Label(window, image=img, height=520, width=550).place(x=200, y=100)

# Create a frame for the login form
frame = Frame(window, height=525, width=550, bg='white')
frame.place(x=750, y=100)

# Heading for the login form
heading = Label(frame, pady=50, padx=20, text='Log in', fg='#00008b', bg='white',
                font=('Microsoft YaHei UI Light', 28, 'bold'))
heading.place(x=200, y=5)

# Entry for the username


user = Entry(frame, width=25, fg='black', bg='white', font=('Microsoft YaHei UI Light', 20))
user.place(x=60, y=180)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=390, height=2, bg='#00008b').place(x=55, y=230)

# Entry for the password


pwd = Entry(frame, width=25, fg='black', bg='white', font=('Microsoft YaHei UI Light', 20))
pwd.place(x=60, y=270)
pwd.insert(0, 'Password')
pwd.bind('<FocusIn>', on_enter_password)
pwd.bind('<FocusOut>', on_leave_password)
Frame(frame, width=390, height=2, bg='#00008b').place(x=55, y=330)

# Sign-in button
Button(frame, width=35, pady=8, text='Sign in', bg='#3030f8', fg='white', border=0, font='20', command=signin).place(x=50, y=380)

# Label for sign-up link
label = Label(frame, text='Don\'t have an account?', font=('Microsoft YaHei UI Light', 11), bg='white')
label.place(x=50, y=440)

# Sign-up link button
sign_up = Button(frame, text='Sign-up', border=0, bg='white', fg='#3030f8', font=('Microsoft YaHei UI Light', 11),command=signup)
sign_up.place(x=212, y=435)


# Forgot Password link button
forgot_pwd = Button(frame, fg='#3030f8', font=('Microsoft YaHei UI Light', 11), border=0, bg='white', text='Forgot Password?')
forgot_pwd.place(x=350, y=440)

# Start the main loop
window.mainloop()

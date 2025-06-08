import customtkinter as Ctk
from PIL import Image
from tkinter import messagebox, StringVar
import mysql.connector  # Correct import for MySQL
import os
import re


def Signin():
    root.destroy()  # Close the current window
    os.system("python Signin.py")  # Open Forgot Password GUI

# Function to handle signup
def signUp():
    name = nameEntry.get()
    email = emailEntry.get() if emailEntry.get() else None
    mobile = mobilenoEntry.get()
    password = passwordEntry.get() if passwordEntry.get() else mobile
    confirm_password = cpassEntry.get() if cpassEntry.get() else mobile
    role = role_var.get()

    if not name or not mobile:
        messagebox.showerror("Error", "Name and Mobile Number are required!")
        return

    if email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format!")
            return


    if not name.isalpha() and ' ' not in name:
        messagebox.showerror("Error", "Name should only contain alphabets and spaces!")
        return

    if not mobile.isdigit() or len(mobile) != 10:
        messagebox.showerror("Error", "Invalid mobile number! Enter a 10-digit number.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM UserSignUp WHERE Mobile = %s", (mobile,))
        user_exists = cursor.fetchone()

        cursor.execute("SELECT * FROM DoctorSignUp WHERE Mobile = %s", (mobile,))
        doctor_exists = cursor.fetchone()

        if user_exists or doctor_exists:
            messagebox.showerror("Error", "Mobile number already registered! Please use a different number.")
            return

        if role == "User":
            query = "INSERT INTO UserSignUp (email, name, Mobile, password1) VALUES (%s, %s, %s, %s)"
            values = (email, name, mobile, password)

        elif role == "Admin":
            query = "INSERT INTO DoctorSignUp (name, email, Mobile, password1) VALUES (%s, %s, %s, %s)"
            values = (name, email, mobile, password)

        cursor.execute(query, values)
        conn.commit()

        messagebox.showinfo("Success", f"{role} registered successfully!")
        Signin()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# GUI Setup
root = Ctk.CTk()
root.geometry("1160x718")
root.title("Sign Up Page")
root.resizable(0, 0)

image = Ctk.CTkImage(Image.open(r"C:\Users\vighn\Documents\project\apache.png"), size=(1160, 718))
image_label = Ctk.CTkLabel(root, image=image, text='')
image_label.place(x=0, y=0)

siguframe = Ctk.CTkFrame(root, fg_color='white', bg_color='white', width=500, height=570)
siguframe.place(x=330, y=70)

headinglabel = Ctk.CTkLabel(root, text='Sign Up', bg_color='white', font=('Ariel Black', 40, 'bold'), text_color='black')
headinglabel.place(x=520, y=90)

nam = Ctk.CTkLabel(root, text='Name', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
nam.place(x=365, y=180)
nameEntry = Ctk.CTkEntry(root, placeholder_text='Enter your name', fg_color='white', bg_color='white', width=230, text_color='black')
nameEntry.place(x=575, y=180)

mail = Ctk.CTkLabel(root, text='Email (Optional)', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
mail.place(x=365, y=248)
emailEntry = Ctk.CTkEntry(root, placeholder_text='Enter your email (optional)', fg_color='white', bg_color='white', width=230, text_color='black')
emailEntry.place(x=575, y=248)

mob = Ctk.CTkLabel(root, text='Mobile No', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
mob.place(x=365, y=316)
mobilenoEntry = Ctk.CTkEntry(root, placeholder_text='Enter your mobile no', fg_color='white', bg_color='white', width=230, text_color='black')
mobilenoEntry.place(x=575, y=316)

pas = Ctk.CTkLabel(root, text='Password (Optional)', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
pas.place(x=365, y=384)
passwordEntry = Ctk.CTkEntry(root, placeholder_text='Enter your password (optional)', fg_color='white', bg_color='white', width=230, show='*', text_color='black')
passwordEntry.place(x=575, y=384)

cpas = Ctk.CTkLabel(root, text='Confirm Password', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
cpas.place(x=365, y=452)
cpassEntry = Ctk.CTkEntry(root, placeholder_text='Re-enter your password (optional)', fg_color='white', bg_color='white', width=230, show='*', text_color='black')
cpassEntry.place(x=575, y=452)

rol = Ctk.CTkLabel(root, text='Select Role', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
rol.place(x=365, y=520)
role_var = StringVar(value="User")  # Default role
role_options = ["User", "Admin"]
role_menu = Ctk.CTkOptionMenu(root, variable=role_var, values=role_options, width=230)
role_menu.place(x=575, y=520)

loginbutton = Ctk.CTkButton(root, text='Sign Up', font=('Arial', 20, 'bold'), bg_color='white', cursor='hand2',
                            command=signUp ,corner_radius=20)
loginbutton.place(x=505, y=575)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Window dimensions
window_width = 1160
window_height = 718

# Calculate x and y coordinates for the window to be centered
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()

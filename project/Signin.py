import customtkinter as Ctk
from PIL import Image
from tkinter import messagebox, StringVar
import mysql.connector  # Correct import for MySQL
import os
import globals



def forgot_password():
    root.destroy()
    os.system("python smsverification.py")  # Opens Forgot Password GUI


def signIn():
    mobile = mobileEntry.get()
    password = passwordEntry.get()
    role = role_var.get()

    if not mobile or not password:
        messagebox.showerror("Error", "Mobile Number and Password are required!")
        return

    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")
        cursor = conn.cursor()

        if role == "User":
            query = "SELECT * FROM UserSignUp WHERE Mobile = %s AND password1 = %s"
        elif role == "Admin":
            query = "SELECT * FROM DoctorSignUp WHERE Mobile = %s AND password1 = %s"

        cursor.execute(query, (mobile, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", f"Welcome, {role}!")

            globals.global_mobile = mobile

            if role == "User":

                # Check if mobile exists in doctor table
                query = "SELECT * FROM users WHERE contact_number = %s"
                cursor.execute(query, (mobile,))
                users = cursor.fetchone()

                if users:
                    os.system(f"python userinterface.py {globals.global_mobile}")
                # open full doctor interface
                else:
                    os.system("python userR.py")  # open registration interface


            elif role == "Admin":
                # Check if mobile exists in doctor table
                query = "SELECT * FROM doctor WHERE contact_numberpr = %s"
                cursor.execute(query, (mobile,))
                doctor = cursor.fetchone()

                if doctor:
                    os.system(f"python doctorinterface.py {globals.global_mobile}")
  # open full doctor interface
                else:
                    os.system("python docR.py")  # open registration interface

            else:
                messagebox.showerror("Error", "Invalid credentials! Please try again.")
        else:
            messagebox.showerror("Error", "Invalid credentials! Please try again.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# GUI Setup
root = Ctk.CTk()
root.geometry("1160x718")
root.title("Sign In Page")
root.resizable(0, 0)

image = Ctk.CTkImage(Image.open(r"C:\\Users\\vighn\\Documents\\project\\apache.png"), size=(1160, 718))
image_label = Ctk.CTkLabel(root, image=image, text='')
image_label.place(x=0, y=0)

siguframe = Ctk.CTkFrame(root, fg_color='white', bg_color='white', width=500, height=400)
siguframe.place(x=330, y=150)

headinglabel = Ctk.CTkLabel(root, text='Sign In', bg_color='white', font=('Ariel Black', 40, 'bold'),
                            text_color='black')
headinglabel.place(x=520, y=170)

mob = Ctk.CTkLabel(root, text='Mobile No', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
mob.place(x=365, y=250)
mobileEntry = Ctk.CTkEntry(root, placeholder_text='Enter your mobile no', fg_color='white', bg_color='white', width=230,
                           text_color='black')
mobileEntry.place(x=575, y=250)

pas = Ctk.CTkLabel(root, text='Password', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
pas.place(x=365, y=320)
passwordEntry = Ctk.CTkEntry(root, placeholder_text='Enter your password', fg_color='white', bg_color='white',
                             width=230, show='*', text_color='black')
passwordEntry.place(x=575, y=320)

rol = Ctk.CTkLabel(root, text='Select Role', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
rol.place(x=365, y=390)
role_var = StringVar(value="User")  # Default role
role_options = ["User", "Admin"]
role_menu = Ctk.CTkOptionMenu(root, variable=role_var, values=role_options, width=230)
role_menu.place(x=575, y=390)

loginbutton = Ctk.CTkButton(root, text='Sign In', font=('Arial', 20, 'bold'), bg_color='white', cursor='hand2',
                            command=signIn, corner_radius=20)
loginbutton.place(x=505, y=460)

forgot_pass_button = Ctk.CTkButton(root, text='Forgot Password?', font=('Arial', 14, 'bold'), bg_color='white',
                                   cursor='hand2',
                                   command=forgot_password, fg_color="red", corner_radius=20)
forgot_pass_button.place(x=495, y=510)

# Center the window on screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1160
window_height = 718
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()

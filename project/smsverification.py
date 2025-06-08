import customtkinter as Ctk
from PIL import Image
from tkinter import messagebox
import random
import mysql.connector
from twilio.rest import Client
import os

def open_forgot_password():
    root.destroy()  # Close the current window
    os.system("python forgot_password_gui.py")  # Open Forgot Password GUI

def Signin():
    root.destroy()  # Close the current window
    os.system("python Signin.py")  # Open Forgot Password GUI


# Twilio credentials (Replace with your details)
ACCOUNT_SID = "ACc9fd0ba69b60e798acdcb75decca7ec9"
AUTH_TOKEN = "674da2c5a0ebf67501abad5801b2cfd0"
TWILIO_PHONE_NUMBER = "+15592546692"

# Database Connection Function
def connect_db():
    return mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")

# Function to send OTP
def send_otp():
    global generated_otp, entered_mobile
    entered_mobile = mobileEntry.get()

    if not entered_mobile.isdigit() or len(entered_mobile) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit mobile number!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT mobile FROM UserSignUp WHERE mobile = %s", (entered_mobile,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            messagebox.showerror("Error", "Mobile number not found!")
            return
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return

    generated_otp = str(random.randint(1000, 9999))

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP for password reset is: {generated_otp}",
            from_=TWILIO_PHONE_NUMBER,
            to="+91" + entered_mobile
        )
        messagebox.showinfo("Success", "OTP sent to your mobile number!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {e}")

# Function to verify OTP
def verify_otp():
    entered_otp = otpEntry.get()
    if entered_otp == generated_otp:
        messagebox.showinfo("Success", "OTP Verified! You can reset your password.")
        reset_password()
    else:
        messagebox.showerror("Error", "Invalid OTP!")

# Function to reset password
def reset_password():
    reset_window = Ctk.CTkToplevel()
    reset_window.geometry("400x300")
    reset_window.title("Reset Password")

    Ctk.CTkLabel(reset_window, text="Enter New Password", font=("Arial", 14)).pack(pady=5)
    new_password_entry = Ctk.CTkEntry(reset_window, width=300, show="*")
    new_password_entry.pack(pady=5)

    def update_password():
        new_password = new_password_entry.get()
        if not new_password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "UPDATE UserSignUp SET password1 = %s WHERE mobile = %s"
            cursor.execute(query, (new_password, entered_mobile))
            conn.commit()
            messagebox.showinfo("Success", "Password Reset Successfully!")
            reset_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    Ctk.CTkButton(reset_window, text="Reset Password", command=update_password).pack(pady=10)

# GUI Setup
root = Ctk.CTk()
root.geometry("1160x718")
root.title("Forgot Password - OTP via Mobile")
root.resizable(0, 0)

image = Ctk.CTkImage(Image.open(r"C:\\Users\\vighn\\Documents\\project\\apache.png"), size=(1160, 718))
image_label = Ctk.CTkLabel(root, image=image, text='')
image_label.place(x=0, y=0)

mobileFrame = Ctk.CTkFrame(root, fg_color='white', bg_color='white', width=500, height=400)
mobileFrame.place(x=330, y=150)

headingLabel = Ctk.CTkLabel(root, text='OTP via Mobile', bg_color='white', font=('Ariel Black', 40, 'bold'), text_color='black')
headingLabel.place(x=450, y=170)

mobileLabel = Ctk.CTkLabel(root, text='Mobile No', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
mobileLabel.place(x=365, y=260)
mobileEntry = Ctk.CTkEntry(root, placeholder_text='Enter your mobile no', fg_color='white', bg_color='white', width=230, text_color='black')
mobileEntry.place(x=575, y=260)

otpButton = Ctk.CTkButton(root, text='Get OTP', font=('Arial', 20, 'bold'), bg_color='white', cursor='hand2', command=send_otp ,corner_radius=20)
otpButton.place(x=505, y=320)

otpLabel = Ctk.CTkLabel(root, text='Enter OTP', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
otpLabel.place(x=365, y=380)
otpEntry = Ctk.CTkEntry(root, placeholder_text='Enter OTP', fg_color='white', bg_color='white', width=230, text_color='black')
otpEntry.place(x=575, y=380)

verifyButton = Ctk.CTkButton(root, text='Verify OTP', font=('Arial', 20, 'bold'), bg_color='white', cursor='hand2', command=verify_otp,corner_radius=20)
verifyButton.place(x=505, y=440)

tryAnotherButton = Ctk.CTkButton(root, text='Try Another Way', font=('Arial', 16, 'bold'), bg_color='white', cursor='hand2' ,command=open_forgot_password )
tryAnotherButton.place(x=680, y=500)

BackToLogin = Ctk.CTkButton(root, text='Back To Login', font=('Arial', 16, 'bold'), bg_color='white', cursor='hand2' ,command=Signin )
BackToLogin.place(x=340, y=500)

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

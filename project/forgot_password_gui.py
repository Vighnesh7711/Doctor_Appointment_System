import customtkinter as Ctk
from PIL import Image
from tkinter import messagebox
import random
import smtplib
import mysql.connector
import os

def smsverification():
    root.destroy()  # Close the current window
    os.system("python smsverification.py")  # Open Forgot Password GUI

def Signin():
    root.destroy()  # Close the current window
    os.system("python Signin.py")  # Open Forgot Password GUI

smsverification
# Database Connection Function
def connect_db():
    return mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")

# Function to send OTP
def send_otp():
    global generated_otp, entered_email
    entered_email = emailEntry.get()

    if not entered_email:
        messagebox.showerror("Error", "Please enter an email!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM UserSignUp WHERE email = %s", (entered_email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            messagebox.showerror("Error", "Email not found!")
            return
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return

    generated_otp = str(random.randint(1000, 9999))

    sender_email = "studynotes132@gmail.com"
    sender_password = "whqp htdg qqsr sisy"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        subject = "OTP for Password Reset"
        message = f"Subject: {subject}\n\nYour OTP is: {generated_otp}"
        server.sendmail(sender_email, entered_email, message)
        server.quit()
        messagebox.showinfo("Success", "OTP sent to your email!")
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
            query = "UPDATE UserSignUp SET password1 = %s WHERE email = %s"
            cursor.execute(query, (new_password, entered_email))
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
root.title("Forgot Password - OTP via Email")
root.resizable(0, 0)

image = Ctk.CTkImage(Image.open(r"C:\\Users\\vighn\\Documents\\project\\apache.png"), size=(1160, 718))
image_label = Ctk.CTkLabel(root, image=image, text='')
image_label.place(x=0, y=0)

emailFrame = Ctk.CTkFrame(root, fg_color='white', bg_color='white', width=500, height=400)
emailFrame.place(x=330, y=150)

headingLabel = Ctk.CTkLabel(root, text='OTP via Email', bg_color='white', font=('Ariel Black', 40, 'bold'), text_color='black')
headingLabel.place(x=450, y=170)

emailLabel = Ctk.CTkLabel(root, text='Email', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
emailLabel.place(x=365, y=260)
emailEntry = Ctk.CTkEntry(root, placeholder_text='Enter your email', fg_color='white', bg_color='white', width=230, text_color='black')
emailEntry.place(x=575, y=260)

otpButton = Ctk.CTkButton(root, text='Get OTP', font=('Arial', 20, 'bold'), bg_color='white', cursor='hand2',corner_radius=20, command=send_otp)
otpButton.place(x=505, y=320)

otpLabel = Ctk.CTkLabel(root, text='Enter OTP', bg_color='white', font=('Ariel Black', 20, 'bold'), text_color='black')
otpLabel.place(x=365, y=380)
otpEntry = Ctk.CTkEntry(root, placeholder_text='Enter OTP', fg_color='white', bg_color='white', width=230, text_color='black')
otpEntry.place(x=575, y=380)

verifyButton = Ctk.CTkButton(root, text='Verify OTP', font=('Arial', 20, 'bold'), bg_color='white',corner_radius=20, cursor='hand2', command=verify_otp)
verifyButton.place(x=505, y=440)

tryAnotherButton = Ctk.CTkButton(root, text='Try Another Way', font=('Arial', 16, 'bold'), bg_color='white', cursor='hand2' ,command=smsverification)
tryAnotherButton.place(x=680, y=500)

BackToLogin = Ctk.CTkButton(root, text='Back To Login', font=('Arial', 16, 'bold'), bg_color='white', cursor='hand2' ,command=Signin)
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
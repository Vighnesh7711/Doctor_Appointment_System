import customtkinter as ctk
from PIL import Image
import os

def Signin():
    os.system(f"python Signin.py ")
    root.destroy()

def Signup1():
    os.system(f"python Signup1.py ")
    root.destroy()

# Initialize main window
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Doctor Appointment System")
root.geometry("1280x720")

# Load background image
bg_image = ctk.CTkImage(Image.open(r"C:\Users\vighn\Documents\project\home_page.png"), size=(1280, 720))
bg_label = ctk.CTkLabel(root, image=bg_image, text="")
bg_label.place(x=0, y=0)

# Function to handle clicks (will show login/signup based on button pressed)
def on_click(event):
    # You can add logic here if you want clicks on image to do something
    pass

# Bind click event to background image
bg_label.bind("<Button-1>", on_click)

# Create login/signup buttons next to "Home" text
button_frame = ctk.CTkFrame(root, fg_color="#0A407F")
button_frame.place(x=220, y=20)  # Position near the "Home" text

login_btn = ctk.CTkButton(button_frame,
                         text="Login",
                         width=100,
                         bg_color="#0A407F",fg_color="#0A407F", font=("Arial", 20, 'bold'),
                         command=Signin)
login_btn.pack(side="left", padx=5)

signup_btn = ctk.CTkButton(button_frame,
                          text="Sign Up",
                          width=100,
                          bg_color="#0A407F",fg_color="#0A407F", font=("Arial", 20, 'bold'),
                          command=Signup1)
signup_btn.pack(side="left", padx=5)

root.mainloop()
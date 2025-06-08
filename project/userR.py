import mysql.connector
import customtkinter as Ctk
from tkinter import StringVar, IntVar, messagebox, Toplevel, filedialog
import sys
from customtkinter import CTkImage
from tkcalendar import Calendar
from PIL import Image, ImageTk
import os

import globals


if len(sys.argv) > 1:
    globals.global_mobile = sys.argv[1]
    print("Doctor mobile from command line:", globals.global_mobile)
else:
    print("No doctor mobile received.")

mobile_number = globals.global_mobile



# Create folders for storing images & PDFs
DATA_FOLDER = "doctor_data"
IMAGE_FOLDER = os.path.join(DATA_FOLDER, "images")
PDF_FOLDER = os.path.join(DATA_FOLDER, "pdfs")

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

# Global variables for image & PDF paths
image_path = None
pdf_path = None


# MySQL Connection
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="student",
            database="DocDB"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


# Function to register doctor
def register_doctor():
    global image_path, pdf_path

    name = name_var.get().strip()
    email = email_var.get().strip()
    contact_number = contact_var.get().strip()
    address = address_var.get("1.0", "end").strip()
    dobpr = dob_var.get().strip()

    if not all([name, email, contact_number, address, dobpr]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if not image_path:
        messagebox.showerror("Error", "Please select a profile image!")
        return



    try:
        db = connect_db()
        if db is None:
            return

        cursor = db.cursor()

        # Get email from DoctorSignUp table
        cursor.execute("SELECT email FROM UserSignUp WHERE user_id = (SELECT MAX(user_id) FROM UserSignUp)")
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "No user email found in UserSignUp!")
            return

        email = result[0]

        query = """
            INSERT INTO Users (Name1 , email, contact_number, address,
                                 DOB, imagepr)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            name, email, contact_number, address
            , dobpr, image_path
        )

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "User Registered Successfully!")
        cursor.close()
        db.close()
        root.destroy()

        image_path = None
        pdf_path = None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")



# Function to select an image
def select_image():
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        image_filename = os.path.basename(file_path)
        new_image_path = os.path.join(IMAGE_FOLDER, image_filename)

        try:
            img = Image.open(file_path)
            img = img.resize((100, 100))
            img.save(new_image_path)
            image_path = new_image_path

            ctk_image = CTkImage(light_image=img, size=(100, 100))
            image_label.configure(image=ctk_image)
            image_label.image = ctk_image

            print("Image saved at:", new_image_path)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not save image: {e}")


# Function to open calendar and select DOB
def open_calendar():
    def date_selected():
        selected_date = cal.get_date()
        dob_var.set(selected_date)
        calendar_window.destroy()

    calendar_window = Toplevel(root)
    calendar_window.title("Select Date of Birth")
    calendar_window.geometry("400x400")
    calendar_window.configure(bg="#2b2b2b")

    cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 12))
    cal.pack(pady=20)

    Ctk.CTkButton(calendar_window, text="Select Date", command=date_selected).pack(pady=10)




# GUI Setup
root = Ctk.CTk()
root.geometry("1160x718")
root.title("Sign Up Page")
root.resizable(0, 0)

# Background Image
image = Ctk.CTkImage(Image.open("C:/Users/vighn/Documents/project/apache.png"), size=(1160, 718))
image_label = Ctk.CTkLabel(root, image=image, text='')
image_label.place(x=0, y=0)

# Variables
name_var = StringVar()
email_var = StringVar()
contact_var = StringVar()
address_var = StringVar()
experience_var = StringVar()
dob_var = StringVar()

# Signup Frame
siguframe = Ctk.CTkFrame(root, fg_color='white', width=500, height=600)
siguframe.place(x=230, y=70)

# Profile Photo Upload
photo_frame = Ctk.CTkFrame(siguframe, fg_color="white", width=120, height=120)
photo_frame.place(x=200, y=20)

image_label = Ctk.CTkLabel(photo_frame, text="", width=120, height=120, fg_color="gray")
image_label.place(x=10,y=10)
Ctk.CTkButton(siguframe, text="Upload Image", command=select_image).place(x=190,y=160)

# Form Fields
Ctk.CTkLabel(siguframe, text="Name:",text_color="black",font=('Ariel Black', 15, 'bold')).place(x=25, y=200)
Ctk.CTkEntry(siguframe, textvariable=name_var, width=300,fg_color="white",text_color="black").place(x=160, y=200)

Ctk.CTkLabel(siguframe, text="Email:",text_color="black",font=('Ariel Black', 15, 'bold')).place(x=25, y=250)
Ctk.CTkEntry(siguframe, textvariable=email_var, width=300,fg_color="white",text_color="black").place(x=160, y=250)

Ctk.CTkLabel(siguframe, text="Contact Number:",text_color="black",font=('Ariel Black', 15, 'bold')).place(x=25, y=300)
Ctk.CTkEntry(siguframe, textvariable=contact_var, width=300,fg_color="white",text_color="black").place(x=160, y=300)

Ctk.CTkLabel(siguframe, text="Address:", text_color="black", font=('Ariel Black', 15, 'bold')).place(x=25, y=400)
address_var = Ctk.CTkTextbox(siguframe, height=110, width=300,fg_color="white", text_color="black" ,border_color="black",border_width=2)
address_var.place(x=160, y=400)

Ctk.CTkLabel(siguframe, text="Date of Birth:",text_color="black",font=('Ariel Black', 15, 'bold')).place(x=25, y=350)
Ctk.CTkEntry(siguframe, textvariable=dob_var, state="readonly", width=200,fg_color="white",text_color="black").place(x=160, y=350)
Ctk.CTkButton(siguframe, text="Select Date", command=open_calendar,width=100).place(x=370, y=350)


Ctk.CTkButton(siguframe, text="SUBMIT", command=register_doctor).place(x=180, y=530)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Window dimensions
window_width = 960
window_height = 718

# Calculate x and y coordinates for the window to be centered
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


root.mainloop()
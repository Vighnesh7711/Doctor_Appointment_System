import mysql.connector
import customtkinter as Ctk
from tkinter import StringVar, IntVar, messagebox, Toplevel
from tkcalendar import Calendar
from datetime import datetime

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
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None


# Function to open calendar and select DOB
def open_calendar():
    def date_selected():
        selected_date = cal.get_date()  # Get selected date
        dob_var.set(selected_date)  # Set selected date in the entry field
        calendar_window.destroy()  # Close the calendar window

    calendar_window = Toplevel(root)
    calendar_window.title("Select Date of Birth")
    calendar_window.geometry("400x400")
    calendar_window.configure(bg="#2b2b2b")  # Dark mode background

    # Frame for Calendar
    cal_frame = Ctk.CTkFrame(calendar_window, fg_color="#1e1e1e", corner_radius=10)
    cal_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Calendar Widget
    cal = Calendar(
        cal_frame,
        selectmode="day",
        date_pattern="yyyy-mm-dd",
        font=("Arial", 12),
        background="#444",
        foreground="white",
        headersbackground="#222",
        headersforeground="white",
        selectbackground="#008080",
        normalbackground="#333",
        weekendbackground="#444",
        weekendforeground="white"
    )
    cal.pack(pady=20)

    # Stylish Select Button
    select_btn = Ctk.CTkButton(
        cal_frame,
        text="Select Date",
        command=date_selected,
        fg_color="#008080",
        hover_color="#006060",
        text_color="white",
        corner_radius=8,
        width=120
    )
    select_btn.pack(pady=10)


# Function to register doctor
def register_doctor():
    name = name_var.get().strip()
    specialization = specialization_var.get().strip()
    contact_number = contact_var.get().strip()
    clinic_address = address_var.get().strip()
    experience = experience_var.get()
    dob = dob_var.get().strip()

    # Input validation
    if not all([name, specialization, contact_number, clinic_address, dob]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if not contact_number.isdigit() or len(contact_number) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit contact number!")
        return

    if not isinstance(experience, int) or experience < 0:
        messagebox.showerror("Error", "Experience must be a positive integer!")
        return

    try:
        db = connect_db()
        if db is None:
            return

        cursor = db.cursor()

        query = """
            INSERT INTO Doctor (name, specialization, contact_number, clinic_address, experience, DOB)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (name, specialization, contact_number, clinic_address, experience, dob)
        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Doctor Registered Successfully!")
        cursor.close()
        db.close()

        # Clear fields after registration
        name_var.set("")
        specialization_var.set("")
        contact_var.set("")
        address_var.set("")
        experience_var.set(0)
        dob_var.set("")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


# Initialize main window
Ctk.set_appearance_mode("dark")
Ctk.set_default_color_theme("green")
root = Ctk.CTk()
root.title("Doctor Registration Form")
root.geometry("500x650")

# Frame for Registration Form
frame = Ctk.CTkFrame(root, fg_color="#2b2b2b", corner_radius=12)
frame.pack(pady=20, padx=20, fill='both', expand=True)

# Heading Label
Ctk.CTkLabel(frame, text="Doctor Registration", font=("Arial", 20, "bold"), text_color="white").pack(pady=10)

# Doctor Name
Ctk.CTkLabel(frame, text="Doctor Name:", text_color="white").pack(pady=5)
name_var = StringVar()
name_entry = Ctk.CTkEntry(frame, textvariable=name_var, width=300)
name_entry.pack(pady=5)

# Specialization
Ctk.CTkLabel(frame, text="Specialization:", text_color="white").pack(pady=5)
specialization_var = StringVar()
specialization_entry = Ctk.CTkEntry(frame, textvariable=specialization_var, width=300)
specialization_entry.pack(pady=5)

# Contact Number
Ctk.CTkLabel(frame, text="Contact Number:", text_color="white").pack(pady=5)
contact_var = StringVar()
contact_entry = Ctk.CTkEntry(frame, textvariable=contact_var, width=300)
contact_entry.pack(pady=5)

# Clinic Address
Ctk.CTkLabel(frame, text="Clinic Address:", text_color="white").pack(pady=5)
address_var = StringVar()
address_entry = Ctk.CTkEntry(frame, textvariable=address_var, width=300)
address_entry.pack(pady=5)

# Experience (in Years)
Ctk.CTkLabel(frame, text="Experience (Years):", text_color="white").pack(pady=5)
experience_var = IntVar(value=0)
experience_entry = Ctk.CTkEntry(frame, textvariable=experience_var, width=300)
experience_entry.pack(pady=5)

# Date of Birth (DOB) with Calendar Button
Ctk.CTkLabel(frame, text="Date of Birth (DOB):", text_color="white").pack(pady=5)
dob_var = StringVar()
dob_entry = Ctk.CTkEntry(frame, textvariable=dob_var, state="readonly", width=300)
dob_entry.pack(pady=5)
Ctk.CTkButton(
    frame, text="Select Date", command=open_calendar, fg_color="#008080",
    hover_color="#006060", text_color="white", corner_radius=8, width=150
).pack(pady=5)

# Register Button
register_button = Ctk.CTkButton(
    frame, text="Register Doctor", command=register_doctor, fg_color="#00cc44",
    hover_color="#009933", text_color="white", corner_radius=8, width=200
)
register_button.pack(pady=20)

# Run Application
root.mainloop()

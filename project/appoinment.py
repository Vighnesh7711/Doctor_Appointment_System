import mysql.connector
import customtkinter as Ctk
from PIL import Image
from tkinter import StringVar, messagebox, Toplevel
from tkcalendar import Calendar
import os
import sys
import globals
import smtplib
from email.message import EmailMessage

if len(sys.argv) > 1:
    globals.global_mobile = sys.argv[1]
    print("user mobile from command line:", globals.global_mobile)
else:
    print("No doctor mobile received.")

mobile_number = globals.global_mobile

# Function to connect to the database
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

# Function to fetch doctors
def fetch_doctors():
    db = connect_db()
    if not db:
        return []
    cursor = db.cursor()
    cursor.execute("SELECT id, namepr FROM doctor")
    doctors = cursor.fetchall()
    cursor.close()
    db.close()
    return doctors

# Function to fetch available time slots
def fetch_time_slots(doctor_id, selected_date):
    db = connect_db()
    if not db:
        return []
    cursor = db.cursor()
    cursor.execute("SELECT time_slot FROM appointments1 WHERE doctor_id = %s AND date = %s", (doctor_id, selected_date))
    booked_slots = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()
    all_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "02:00 PM", "03:00 PM", "04:00 PM"]
    return [slot for slot in all_slots if slot not in booked_slots]

# Function to open calendar
def open_calendar():
    def date_selected():
        selected_date = cal.get_date()
        date_var.set(selected_date)
        calendar_window.destroy()
        show_available_slots()

    calendar_window = Toplevel(root)
    calendar_window.title("Select Date")
    cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20)
    Ctk.CTkButton(calendar_window, text="Select", command=date_selected).pack(pady=10)

# Function to display available slots
def show_available_slots():
    selected_doctor = doctor_var.get()
    selected_date = date_var.get()
    if not selected_doctor or not selected_date:
        return

    doctor_id = next((d[0] for d in doctors if d[1] == selected_doctor), None)
    available_slots = fetch_time_slots(doctor_id, selected_date)


    for widget in slots_frame.winfo_children():
        widget.destroy()


    rows = (len(available_slots) // 3) + (1 if len(available_slots) % 3 != 0 else 0)

    for index, slot in enumerate(available_slots):
        row = index // 3
        col = index % 3

        Ctk.CTkButton(slots_frame, text=slot, command=lambda s=slot: book_appointment(s), width=100).grid(row=row, column=col, padx=5, pady=5)


# Function to book an appointment
def book_appointment(time_slot):
    doctor_id = next((d[0] for d in doctors if d[1] == doctor_var.get()), None)
    selected_date = date_var.get()
    patient_name = patient_var.get().strip()
    description = description_box.get("1.0", "end").strip()
    contact_number = globals.global_mobile  # Get the mobile number from globals

    if not patient_name:
        messagebox.showerror("Error", "Enter patient name!")
        return
    if not description:
        messagebox.showerror("Error", "Enter a description of the issue!")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO appointments1 (doctor_id, date, time_slot, patient_name, description,contact_number) VALUES (%s, %s, %s, %s, %s, %s)",
        (doctor_id, selected_date, time_slot, patient_name, description, contact_number)
    )
    db.commit()
    cursor.close()
    db.close()
    messagebox.showinfo("Success", "Appointment Booked Successfully!")
    show_available_slots()

# GUI setup
Ctk.set_appearance_mode("light")
root = Ctk.CTk()
root.geometry("1160x718")
root.title("Doctor Appointment System")
root.resizable(0, 0)

# Background image
image = Ctk.CTkImage(Image.open(r"C:\\Users\\vighn\\Documents\\project\\apache.png"), size=(1160, 718))
image_label = Ctk.CTkLabel(root, image=image, text='')
image_label.place(x=0, y=0)

# Main Frame
frame = Ctk.CTkFrame(root, fg_color='white', width=500, height=600)
frame.place(x=250, y=60)

# UI Elements
doctors = fetch_doctors()

Ctk.CTkLabel(frame, text='Select Doctor', font=('Ariel Black', 20), text_color='black').pack(pady=5)
doctor_var = StringVar()
doctor_menu = Ctk.CTkComboBox(frame, values=[d[1] for d in doctors], variable=doctor_var, command=lambda _: show_available_slots())
doctor_menu.pack(pady=5)

Ctk.CTkLabel(frame, text='Select Date', font=('Ariel Black', 20), text_color='black').pack(pady=5)
date_var = StringVar()
date_entry = Ctk.CTkEntry(frame, textvariable=date_var, state="readonly")
date_entry.pack(pady=5)
Ctk.CTkButton(frame, text="Pick Date", command=open_calendar, corner_radius=20).pack(pady=5)

Ctk.CTkLabel(frame, text='Patient Name', font=('Ariel Black', 20), text_color='black').pack(pady=5)
patient_var = StringVar()
patient_entry = Ctk.CTkEntry(frame, textvariable=patient_var)
patient_entry.pack(pady=5)

Ctk.CTkLabel(frame, text='Describe Your Issue', font=('Ariel Black', 20), text_color='black').pack(pady=5)
description_box = Ctk.CTkTextbox(frame, height=50, width=400 ,border_color="grey",border_width=2)
description_box.pack(pady=5)

Ctk.CTkLabel(frame, text='Available Time Slots', font=('Ariel Black', 20), text_color='black').pack(pady=5)
slots_frame = Ctk.CTkFrame(frame)
slots_frame.pack(pady=10,padx=10, fill='x')

# Centering the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 900
window_height = 718
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()
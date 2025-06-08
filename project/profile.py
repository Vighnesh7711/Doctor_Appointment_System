import customtkinter as Ctk
from tkinter import Scrollbar, messagebox
from PIL import Image, ImageTk
import mysql.connector


def admin_profile():
    root = Ctk.CTk()
    root.title("Admin Profile")
    root.geometry("800x600")

    def fetch_doctor_details():
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Doctor")
            doctors = cursor.fetchall()
            cursor.close()
            conn.close()
            return doctors
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def fetch_staff_details(doctor_id):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM StaffDetails WHERE doctor_id = %s", (doctor_id,))
            staff = cursor.fetchall()
            cursor.close()
            conn.close()
            return staff
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def add_staff(doctor_id):
        # Logic to add staff to the database
        pass

    def modify_staff(staff_id):
        # Logic to modify staff details
        pass

    def delete_staff(staff_id):
        # Logic to delete staff
        pass

    frame = Ctk.CTkScrollableFrame(root, width=780, height=550)
    frame.pack(pady=10, padx=10, fill='both', expand=True)

    doctors = fetch_doctor_details()
    for doctor in doctors:
        doc_id, name, specialization, age, phone, address, email, image_path = doctor

        doc_frame = Ctk.CTkFrame(frame, fg_color='white', width=750, height=200)
        doc_frame.pack(pady=10)

        img = Image.open(image_path)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        img_label = Ctk.CTkLabel(doc_frame, image=img, text='')
        img_label.image = img
        img_label.place(x=10, y=10)

        details_text = f"Name: {name}\nSpecialization: {specialization}\nAge: {age}\nPhone: {phone}\nAddress: {address}\nEmail: {email}"
        details_label = Ctk.CTkLabel(doc_frame, text=details_text, text_color='black', font=('Arial', 12))
        details_label.place(x=120, y=10)

        staff = fetch_staff_details(doc_id)
        staff_text = "Staff:\n" + "\n".join([f"{s[2]} - {s[3]}" for s in staff])
        staff_label = Ctk.CTkLabel(doc_frame, text=staff_text, text_color='black', font=('Arial', 12))
        staff_label.place(x=120, y=100)

        add_btn = Ctk.CTkButton(doc_frame, text='Add Staff', command=lambda d=doc_id: add_staff(d))
        add_btn.place(x=600, y=10)

        modify_btn = Ctk.CTkButton(doc_frame, text='Modify Staff', command=lambda d=doc_id: modify_staff(d))
        modify_btn.place(x=600, y=50)

        delete_btn = Ctk.CTkButton(doc_frame, text='Delete Staff', command=lambda d=doc_id: delete_staff(d))
        delete_btn.place(x=600, y=90)

    root.mainloop()


admin_profile()

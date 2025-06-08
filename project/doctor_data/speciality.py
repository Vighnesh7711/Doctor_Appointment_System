import tkinter as tk
from tkinter import ttk
import mysql.connector


# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="student",
        database="docDB"
    )


def get_specializations():
    """ Fetch unique doctor specializations from the database """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT specialization FROM Doctor")
    specializations = ["All"] + [row[0] for row in cursor.fetchall()]
    conn.close()
    return specializations


def get_doctors(specialty):
    """ Fetch doctors based on the selected specialty """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if specialty == "All":
        cursor.execute("SELECT name, specialization FROM Doctor")
    else:
        cursor.execute("SELECT name, specialization FROM Doctor WHERE specialization = %s", (specialty,))

    doctors = cursor.fetchall()
    conn.close()
    return doctors


def show_doctor_dashboard(frame):
    def update_display(specialty):
        """ Display only doctors of the selected specialty """
        for widget in scroll_frame.winfo_children():
            widget.destroy()  # Clear previous doctors

        doctors = get_doctors(specialty)
        for doctor in doctors:
            tk.Label(scroll_frame, text=f"Dr. {doctor['name']} - {doctor['specialization']}", font=("Arial", 12)).pack(
                pady=5)

    # Get specializations dynamically from the database
    specializations = get_specializations()

    # Dropdown for selecting specialty
    selected_specialty = tk.StringVar(value="All")
    specialty_dropdown = ttk.Combobox(frame, textvariable=selected_specialty, values=specializations, state="readonly")
    specialty_dropdown.pack(pady=10)
    specialty_dropdown.bind("<<ComboboxSelected>>", lambda e: update_display(selected_specialty.get()))

    # Scrollable Canvas
    canvas = tk.Canvas(frame)
    v_scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    h_scrollbar = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Pack elements
    specialty_dropdown.pack()
    canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")

    # Initial doctor display (show all doctors first)
    update_display("All")

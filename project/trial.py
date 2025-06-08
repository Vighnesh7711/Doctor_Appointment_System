import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import globals  # make sure this has global_mobile = "" defined
import os
import webbrowser

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DoctorInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Doctor Dashboard")
        self.geometry("1000x600")

        self.mobile_number = globals.global_mobile

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

        self.label = ctk.CTkLabel(self.sidebar, text=f"Doctor\n{self.mobile_number}", font=("Arial", 16))
        self.label.pack(pady=20)

        self.btn_appointments = ctk.CTkButton(self.sidebar, text="Appointments", command=self.show_appointments)
        self.btn_appointments.pack(pady=10)

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout)
        self.btn_logout.pack(pady=10)

        self.show_appointments()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="your_database_name"  # change this to your DB
        )

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_appointments(self):
        self.clear_main_frame()

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM appointments1 WHERE doctor_mobile = %s"
            cursor.execute(query, (self.mobile_number,))
            appointments = cursor.fetchall()

            if not appointments:
                ctk.CTkLabel(self.main_frame, text="No Appointments Found").pack(pady=20)
                return

            for i, appointment in enumerate(appointments):
                frame = ctk.CTkFrame(self.main_frame)
                frame.pack(padx=20, pady=10, fill="x")

                info = (
                    f"Patient: {appointment['patient_name']}\n"
                    f"Date: {appointment['appointment_date']}\n"
                    f"Time: {appointment['appointment_time']}\n"
                    f"Status: {appointment['status']}"
                )
                ctk.CTkLabel(frame, text=info, anchor="w", justify="left").pack(side="left", padx=10)

                status_menu = ctk.CTkOptionMenu(frame, values=["Pending", "Approved", "Rejected"])
                status_menu.set(appointment["status"])
                status_menu.pack(side="left", padx=10)

                update_btn = ctk.CTkButton(
                    frame,
                    text="Update",
                    command=lambda a_id=appointment["id"], menu=status_menu: self.update_status(a_id, menu.get())
                )
                update_btn.pack(side="left", padx=10)

                # View Report (if file exists)
                report_path = appointment.get("report_path")
                if report_path and os.path.exists(report_path):
                    view_btn = ctk.CTkButton(
                        frame,
                        text="View Report",
                        command=lambda path=report_path: self.open_pdf(path)
                    )
                    view_btn.pack(side="left", padx=10)

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_status(self, appointment_id, new_status):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            update_query = "UPDATE appointments1 SET status = %s WHERE id = %s"
            cursor.execute(update_query, (new_status, appointment_id))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Status updated!")
            self.show_appointments()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_pdf(self, path):
        try:
            webbrowser.open_new(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file.\n{e}")

    def logout(self):
        self.destroy()

if __name__ == "__main__":
    app = DoctorInterface()
    app.mainloop()

import sys
import mysql.connector
import customtkinter as ctk
from tkinter import messagebox, Canvas, Scrollbar, filedialog
import os
from PIL import Image
import webbrowser
import shutil
import globals


if len(sys.argv) > 1:
    globals.global_mobile = sys.argv[1]
    print("user mobile from command line:", globals.global_mobile)
else:
    print("No doctor mobile received.")

mobile_number = globals.global_mobile


def open_demo4():
    os.system(f"python appoinment.py {globals.global_mobile}")

def open_demo44():
    os.system(f"python appoinmentR.py {globals.global_mobile}")

# Database Setup
def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="student", database="DocDB")

def book_appointment(doctor_id, doctor_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments1 (doctor_id, patient_name, contact, appointment_date) VALUES (%s, %s, %s, CURDATE())",
        (doctor_id, "Auto-Registered", "N/A")
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Appointment booked with {doctor_name}!")


def ok():
    os.system(f"python appoinment.py {globals.global_mobile}")


def show_home_dashboard(frame):

    siguframe = ctk.CTkFrame(root, fg_color="#0A407F", bg_color='#0A407F', width=1310, height=70)
    siguframe.place(x=220, y=0)
    label = ctk.CTkLabel(siguframe,text = "Home",
    font = ("Arial", 40, "bold"),
    text_color = "white")
    label.pack(padx=600, pady=10, anchor="center")
    image = ctk.CTkImage(Image.open(r"C:\Users\vighn\Documents\project\head.png"), size=(1310, 418))
    image_label = ctk.CTkLabel(root, image=image, text='')
    image_label.place(x=220, y=70)

    # Inspirational quote frame
    quote_frame = ctk.CTkFrame(root, fg_color="white", bg_color="white", width=900, height=80)
    quote_frame.place(x=280, y=580)
    # Quote text
    quote_text = """\"Quality healthcare begins with timely access to doctors.\n
    Our appointment system bridges the gap between patients and medical expertise.\""""

    quote_label = ctk.CTkLabel(quote_frame,
                               text=quote_text,
                               font=("Arial", 32, "italic"),
                               text_color="#0A407F",
                               justify="center")
    quote_label.pack(pady=20, padx=20)
    book_appo = ctk.CTkButton(root, text='Book Appoinment', font=('Arial', 20, 'bold'), fg_color='#0A407F', cursor='hand2',
                              corner_radius=10, width=140, height=45 ,command=ok)
    book_appo.place(x=750, y=525)




def show_doctor_dashboard(frame):
    label = ctk.CTkLabel(frame, text="Available Doctors", font=("Arial", 22, "bold"))
    label.pack(pady=10)

    # Container frame to hold canvas and scrollbars properly
    container = ctk.CTkFrame(frame)
    container.pack(fill="both", expand=True)

    # Create a Canvas
    canvas = Canvas(container, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbars
    vscrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    vscrollbar.pack(side="right", fill="y")

    hscrollbar = Scrollbar(frame, orient="horizontal", command=canvas.xview)
    hscrollbar.pack(side="bottom", fill="x")

    canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

    # Frame inside canvas for doctor cards
    scroll_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Update scrolling region
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", update_scroll_region)

    # Fetch doctors from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor")
    rows = cursor.fetchall()
    conn.close()

    # Layout doctors in grid
    columns = 4  # Number of doctors per row
    for index, row in enumerate(rows):
        row_pos = index // columns
        col_pos = index % columns

        # Doctor card
        doc_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        doc_frame.grid(row=row_pos, column=col_pos, padx=15, pady=10, sticky="nsew")

        # Doctor details
        ctk.CTkLabel(doc_frame, text=f"Dr. {row[1]}", font=("Arial", 18, "bold")).pack(pady=5)
        ctk.CTkLabel(doc_frame, text=f"Specialty: {row[2]}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkLabel(doc_frame, text=f"Address: {row[3]}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkLabel(doc_frame, text=f"Contact: {row[4]}", font=("Arial", 14)).pack(pady=2)

        # Book Appointment Button
        ctk.CTkButton(doc_frame, text="Book Appointment",command=open_demo4).pack(pady=5)

    # Configure column weights for even distribution
    for i in range(columns):
        scroll_frame.columnconfigure(i, weight=1)


def show_Emergency_dashboard(frame):
    label = ctk.CTkLabel(frame, text="Emergency Appoinment", font=("Arial", 22, "bold"))
    label.pack(pady=10)

    # Container frame to hold canvas and scrollbars properly
    container = ctk.CTkFrame(frame)
    container.pack(fill="both", expand=True)

    # Create a Canvas
    canvas = Canvas(container, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbars
    vscrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    vscrollbar.pack(side="right", fill="y")

    hscrollbar = Scrollbar(frame, orient="horizontal", command=canvas.xview)
    hscrollbar.pack(side="bottom", fill="x")

    canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

    # Frame inside canvas for doctor cards
    scroll_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Update scrolling region
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", update_scroll_region)

    # Fetch doctors from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor")
    rows = cursor.fetchall()
    conn.close()

    # Layout doctors in grid
    columns = 4  # Number of doctors per row
    for index, row in enumerate(rows):
        row_pos = index // columns
        col_pos = index % columns

        # Doctor card
        doc_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        doc_frame.grid(row=row_pos, column=col_pos, padx=15, pady=10, sticky="nsew")

        # Doctor details
        ctk.CTkLabel(doc_frame, text=f"Dr. {row[1]}", font=("Arial", 18, "bold")).pack(pady=5)
        ctk.CTkLabel(doc_frame, text=f"Specialty: {row[2]}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkLabel(doc_frame, text=f"Address: {row[3]}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkLabel(doc_frame, text=f"Contact: {row[4]}", font=("Arial", 14)).pack(pady=2)

        # Book Appointment Button
        ctk.CTkButton(doc_frame, text="Book Appointment",command=open_demo44).pack(pady=5)

    # Configure column weights for even distribution
    for i in range(columns):
        scroll_frame.columnconfigure(i, weight=1)



# Folder to store PDFs
PDF_STORAGE_FOLDER = r"C:\Users\vighn\Documents\project\reports"  # Change path if needed
os.makedirs(PDF_STORAGE_FOLDER, exist_ok=True)


def show_reports_dashboard(frame):
    label = ctk.CTkLabel(frame, text="Manage PDFs", font=("Arial", 22, "bold"))
    label.pack(pady=10)

    # **Frame to hold everything properly**
    container = ctk.CTkFrame(frame)
    container.pack(fill="both", expand=True)

    # **Canvas for displaying PDFs**
    canvas = Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    # **Scrollbars**
    scrollbar_y = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")  # Right side of canvas

    scrollbar_x = Scrollbar(frame, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(side="bottom", fill="x")  # Directly under the canvas

    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scroll_frame = ctk.CTkFrame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def refresh_pdf_list():
        """ Refresh the displayed PDF list """
        for widget in scroll_frame.winfo_children():
            widget.destroy()  # Clear previous list

        pdf_files = os.listdir(PDF_STORAGE_FOLDER)
        if not pdf_files:
            ctk.CTkLabel(scroll_frame, text="No PDFs available.", font=("Arial", 14)).pack(pady=5)
        else:
            for pdf in pdf_files:
                truncated_name = pdf[:10] + "..." if len(pdf) > 10 else pdf

                # **Frame for each PDF entry**
                file_frame = ctk.CTkFrame(scroll_frame)
                file_frame.pack(pady=5, padx=10, fill="x")

                if pdf_icon:
                    icon_label = ctk.CTkLabel(file_frame, image=pdf_icon, text="")
                    icon_label.pack(side="left", padx=10)
                    icon_label.bind("<Button-1>", lambda e, pdf_name=pdf: open_pdf(pdf_name))

                pdf_label = ctk.CTkLabel(file_frame, text=truncated_name, font=("Arial", 12), cursor="hand2")
                pdf_label.pack(side="left", padx=10)
                pdf_label.bind("<Button-1>", lambda e, pdf_name=pdf: open_pdf(pdf_name))

                delete_btn = ctk.CTkButton(file_frame, text="Delete", fg_color="red",
                                           command=lambda pdf_name=pdf: delete_pdf(pdf_name))
                delete_btn.pack(side="right")

    def upload_pdf():
        """ Upload a new PDF to the system folder """
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return  # User canceled

        try:
            shutil.copy(file_path, PDF_STORAGE_FOLDER)
            messagebox.showinfo("Success", "PDF Uploaded Successfully!")
            refresh_pdf_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload PDF: {e}")

    def open_pdf(pdf_name):
        """ Open selected PDF """
        pdf_path = os.path.join(PDF_STORAGE_FOLDER, pdf_name)
        if os.path.exists(pdf_path):
            webbrowser.open(pdf_path)
        else:
            messagebox.showerror("Error", "PDF file not found!")

    def delete_pdf(pdf_name):
        """ Delete selected PDF """
        pdf_path = os.path.join(PDF_STORAGE_FOLDER, pdf_name)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            messagebox.showinfo("Success", "PDF Deleted Successfully!")
            refresh_pdf_list()
        else:
            messagebox.showerror("Error", "PDF file not found!")

    # **Buttons**
    upload_btn = ctk.CTkButton(frame, text="Upload PDF", command=upload_pdf)
    upload_btn.pack(pady=5)

    # Load the list of PDFs initially
    refresh_pdf_list()

def show_about_dashboard(frame):
    # Clear frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create main container frame
    main_frame = ctk.CTkFrame(frame, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create canvas with scrollbar
    canvas = Canvas(main_frame, bg="white", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")

    # Configure canvas scrolling
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # About heading
    heading_frame = ctk.CTkFrame(scrollable_frame, fg_color="#0A407F", height=50)
    heading_frame.pack(fill="x", pady=(0, 15))

    heading_label = ctk.CTkLabel(heading_frame,
                                 text="ABOUT THE PROJECT",
                                 font=("Arial", 40, "bold"),
                                 text_color="white")
    heading_label.pack(padx=370,pady=10)

    # Project content
    content_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
    content_frame.pack(fill="x", padx=10, pady=5)

    about_content = """
DOCTOR APPOINTMENT SYSTEM
(B.E. IT SEM 4 Project 2024-25)

Developed by:
• Vighnesh Gawande (23)
• Vedang Dhuri (20) 
• Prathamesh Gawade (22)
• Tanmay Kamble (34)

Under guidance of:
Prof. Onkar D. Dike
Asst. Professor, IT Dept.
Finolex Academy of Management & Technology

━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM OVERVIEW:

A comprehensive solution designed to:
✓ Streamline doctor-patient appointments
✓ Reduce administrative workload
✓ Improve healthcare accessibility
✓ Enhance patient experience

TECHNOLOGY STACK:
• Frontend: CustomTkinter (Python)
• Backend: Python
• Database: MySQL
• Email: SMTP Integration

KEY FEATURES:
- User-friendly interface
- Secure authentication
- Real-time appointment management
- Automated notifications
- Multi-role access (Patient/Doctor/Admin)
"""

    content_label = ctk.CTkLabel(content_frame,
                                 text=about_content,
                                 font=("Arial", 25),
                                 justify="left")
    content_label.pack(pady=10, padx=10, anchor="w")


def show_contact_dashboard(frame):
    # Clear frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create main container frame
    main_frame = ctk.CTkFrame(frame, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create canvas with scrollbar
    canvas = Canvas(main_frame, bg="white", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")

    # Configure canvas scrolling
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Contact heading
    heading_frame = ctk.CTkFrame(scrollable_frame, fg_color="#0A407F", height=50)
    heading_frame.pack(fill="x", pady=(0, 15))

    heading_label = ctk.CTkLabel(heading_frame,
                                 text="CONTACT INFORMATION",
                                 font=("Arial", 40, "bold"),
                                 text_color="white")
    heading_label.pack(padx=350,pady=10, anchor="center")

    # Contact content
    content_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
    content_frame.pack(fill="x", padx=10, pady=5)

    contact_content = """
DEVELOPMENT TEAM CONTACTS:

Vighnesh Vikas Gawande
• Roll No: 23
• Email: vighnesh.g@famt.ac.in
• Phone: +91 XXXXX XXXXX

Vedang Rajendra Dhuri  
• Roll No: 20
• Email: vedang.d@famt.ac.in
• Phone: +91 XXXXX XXXXX

Prathamesh D. Gawade
• Roll No: 22  
• Email: prathamesh.g@famt.ac.in
• Phone: +91 XXXXX XXXXX

Tanmay Rakesh Kamble
• Roll No: 34
• Email: tanmay.k@famt.ac.in
• Phone: +91 XXXXX XXXXX

━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT GUIDE:

Prof. Onkar D. Dike
Assistant Professor
IT Department
Finolex Academy of Management & Technology
• Email: onkar.dike@famt.ac.in
• Phone: +91-9876543210

━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTITUTION DETAILS:

Finolex Academy of Management & Technology
Department of Information Technology
Ratnagiri, Maharashtra - 415639

• Website: www.famt.ac.in
• Email: itdepartment@famt.ac.in  
• Phone: +91-1234567890
"""

    content_label = ctk.CTkLabel(content_frame,
                                 text=contact_content,
                                 font=("Arial", 25),
                                 justify="left")
    content_label.pack(pady=10, padx=10, anchor="w")



# Initialize main window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Doctor Appointment System")
root.geometry("1280x720")  # Adjusted size

# Load PDF icon
pdf_icon_path = "pdf_icon.png"  # Provide a path to your PDF logo image
pdf_icon = None

if os.path.exists(pdf_icon_path):
    pdf_icon = Image.open(pdf_icon_path)
    pdf_icon = pdf_icon.resize((80, 80))  # Resize for UI
    pdf_icon = ctk.CTkImage(light_image=Image.open("pdf_icon.png"), size=(50, 50))


# Function to switch segments
def show_frame(frame):
    for f in frames.values():
        f.pack_forget()
    frames[frame].pack(fill='both', expand=True, padx=45, pady=20)

# Sidebar with vertical layout
sidebar = ctk.CTkFrame(root, width=250, corner_radius=0)
sidebar.pack(fill='y', side='left')

segment_control = ctk.CTkFrame(sidebar)
segment_control.pack(fill='both', expand=True, pady=20, padx=10)

buttons = ["Home", "Reports", "Doctors", "Emergency", "About", "Contact"]


# List of images and button names
button_data = [
    ("Home", "icon1.png"),
    ("Reports", "icon2.png"),
    ("Doctors", "icon3.png"),
    ("Emergency", "icon4.png"),
    ("About", "icon5.png"),
    ("Contact", "icon6.png")
]
frames = {}
# Create buttons with different images


for btn, img_path in button_data:
    pil_image = Image.open(img_path)
    button_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(25, 25))
    button = ctk.CTkButton(segment_control, text=btn,image=button_image, compound="left", command=lambda b=btn: show_frame(b),fg_color="#0A407F",width=170, height=70, font=('Ariel Black', 20, 'bold'), text_color='white')
    button.pack(fill='x', pady=5, padx=15)

# Function to create frames dynamically
def create_frame(name, text):
    frame = ctk.CTkFrame(root, corner_radius=10, fg_color="transparent")
    if name == "Doctors":
        show_doctor_dashboard(frame)
    elif name == "Home":
        show_home_dashboard(frame)
    elif name == "Reports":
        show_reports_dashboard(frame)
    elif name == "Emergency":
        show_Emergency_dashboard(frame)
    elif name == "Contact":
        show_contact_dashboard(frame)
    elif name == "About":
        show_about_dashboard(frame)
    else:
        label = ctk.CTkLabel(frame, text=text, font=("Arial", 30))
        label.pack(pady=35)
    frames[name] = frame


# Creating all frames
create_frame("Home", "Welcome to Doctor Appointment System!")
create_frame("Reports", "Your Medical Reports")
create_frame("Appointment", "Book an Appointment")
create_frame("Doctors", "")
create_frame("Emergency", "Emergency Contact Information")
create_frame("About", "About Us")
create_frame("Contact", "Contact Us")

# Show default frame
show_frame("Home")

# Run Application
root.mainloop()



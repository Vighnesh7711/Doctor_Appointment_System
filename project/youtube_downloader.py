import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # Import the ttk module for themed widgets
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip

# Check if tkinter is available in the environment
def check_tkinter():
    try:
        import tkinter
    except ModuleNotFoundError:
        raise ImportError("The 'tkinter' module is not available in this environment. Please ensure it is installed and supported.")

check_tkinter()

# Function to extract audio using moviepy
def extract_audio(file_path, output_path):
    try:
        try:
            video = VideoFileClip(file_path)
            audio = video.audio
            audio.write_audiofile(output_path)
            audio.close()
            video.close()
        except OSError:
            audio = AudioFileClip(file_path)
            audio.write_audiofile(output_path)
            audio.close()
    except Exception as e:
        messagebox.showerror("Error", f"Audio extraction failed: {str(e)}")

# Function to handle the download process
def download():
    link = url_entry.get()
    download_type = download_type_var.get()
    resolution = resolution_var.get()
    audio_only = audio_var.get()

    if not link:
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL!")
        return

    format_option = f"bestvideo[height={resolution}]+bestaudio/best" if not audio_only else "bestaudio/best"

    options = {
        'format': format_option,
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [
            lambda d: update_progress(d)
        ],
    }

    folder_name = filedialog.askdirectory(title="Select Download Folder")
    if not folder_name:
        messagebox.showerror("Folder Error", "Please select a valid folder to save the downloads.")
        return

    options['outtmpl'] = os.path.join(folder_name, '%(title)s.%(ext)s')

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            file_path = ydl.prepare_filename(info_dict)

            if audio_only:
                audio_output = os.path.splitext(file_path)[0] + ".mp3"
                extract_audio(file_path, audio_output)
                os.remove(file_path)

        messagebox.showinfo("Download Complete", "Download finished successfully! 🎉")
        progress_label.config(text="Download Complete! 🎉")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Update progress bar and label
def update_progress(d):
    if d['status'] == 'downloading':
        try:
            percent = float(d['_percent_str'].strip('%').strip())
            progress_bar["value"] = percent
            progress_label.config(text=f"Downloading: {percent:.2f}%")
        except (ValueError, KeyError):
            progress_label.config(text="Downloading: Progress unknown")
    elif d['status'] == 'finished':
        progress_label.config(text="Download complete. Finalizing...")

# Create the main window
window = tk.Tk()
window.title("YouTube Video Downloader")
window.geometry("600x400")
window.resizable(True, True)
window.configure(bg="#4CC9FE")

# Configure styles
style = ttk.Style()
style.configure("TLabel", background="#4CC9FE", font=("Arial", 12, "bold"))
style.configure("TCheckbutton", background="#4CC9FE", font=("Arial", 12, "bold"))
style.configure("TButton", font=("Arial", 12, "bold"), foreground="black", background="red")
style.map("TButton", background=[("active", "#cc0000")])

# Font configuration
entry_font = ("Arial", 12)

# Add a label and entry for the YouTube URL
url_label = ttk.Label(window, text="Enter YouTube URL:")
url_label.pack(pady=10)

url_entry = ttk.Entry(window, width=50, font=entry_font)
url_entry.pack(pady=10)

# Add download type selection
download_type_var = tk.StringVar(value="Single Video")
download_type_label = ttk.Label(window, text="Select Download Type:")
download_type_label.pack(pady=5)

download_type_menu = ttk.Combobox(window, textvariable=download_type_var, state="readonly", values=["Single Video", "Playlist"], font=entry_font)
download_type_menu.pack(pady=5)

# Add resolution selection
resolution_var = tk.StringVar(value="720")
resolution_label = ttk.Label(window, text="Select Video Resolution:")
resolution_label.pack(pady=5)

resolution_menu = ttk.Combobox(window, textvariable=resolution_var, state="readonly", values=["2160", "1440", "1080", "720", "480", "360", "240", "144"], font=entry_font)
resolution_menu.pack(pady=5)

# Add audio-only option
audio_var = tk.BooleanVar()
audio_checkbox = ttk.Checkbutton(window, text="Download Audio Only (MP3)", variable=audio_var)
audio_checkbox.pack(pady=10)

# Add a button to start the download process
download_button = ttk.Button(window, text="Download", command=download)
download_button.pack(pady=20)

# Add a progress bar and label to show download progress
progress_label = ttk.Label(window, text="Status: Waiting for input...")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()

import tkinter as tk
from tkinter import messagebox, filedialog, StringVar
from pytube import YouTube
import threading
import os

def download_video(url, path, file_format):
    try:
        yt = YouTube(url)
        if file_format == 'mp4':
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        else:
            video_stream = yt.streams.filter(file_extension=file_format).order_by('resolution').desc().first()

        if video_stream:
            video_stream.download(output_path=path)
            return f"Video downloaded successfully: {yt.title}"
        else:
            return "No stream found for the selected format."

    except Exception as e:
        return f"An error occurred: {e}"

def start_download():
    url = url_entry.get()
    path = path_var.get()
    file_format = format_var.get()

    if url.strip() and path.strip():
        threading.Thread(target=perform_download, args=(url, path, file_format), daemon=True).start()
    else:
        messagebox.showerror("Error", "Please enter a valid URL and select a destination folder.")

def perform_download(url, path, file_format):
    response = download_video(url, path, file_format)
    messagebox.showinfo("Download Status", response)

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create the layout
url_label = tk.Label(root, text="Enter YouTube Video URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

folder_label = tk.Label(root, text="Select Destination Folder:")
folder_label.pack()

path_var = StringVar()
path_entry = tk.Entry(root, textvariable=path_var, width=50)
path_entry.pack()

browse_button = tk.Button(root, text="Browse", command=select_folder)
browse_button.pack()

format_label = tk.Label(root, text="Select File Format:")
format_label.pack()

format_var = StringVar()
format_var.set("mp4")  # default value
format_option = tk.OptionMenu(root, format_var, "mp4", "webm")
format_option.pack()

download_button = tk.Button(root, text="Download Video", command=start_download)
download_button.pack()

# Run the GUI loop
root.mainloop()

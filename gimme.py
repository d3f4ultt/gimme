import argparse
import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, ttk
from pytube import YouTube
import threading
import os

def download_video(url, path, file_format, progress_callback=None):
    try:
        yt = YouTube(url, on_progress_callback=progress_callback)
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

def cli_interface(url, path, file_format):
    response = download_video(url, path, file_format)
    print(response)

def gui_interface():
    def start_download():
        url = url_entry.get()
        path = path_var.get()
        file_format = format_var.get()

        if url.strip() and path.strip():
            threading.Thread(target=perform_download, args=(url, path, file_format), daemon=True).start()
        else:
            messagebox.showerror("Error", "Please enter a valid URL and select a destination folder.")

    def perform_download(url, path, file_format):
        def progress_function(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            progress_bar['value'] = percentage_of_completion
            root.update_idletasks()

        response = download_video(url, path, file_format, progress_function)
        messagebox.showinfo("Download Status", response)
        progress_bar['value'] = 0  # Reset progress bar after download

    def select_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            path_var.set(folder_selected)

    root = tk.Tk()
    root.title("D3f4ult's YouTube Video Downloader")

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
    format_var.set("mp4")
    format_option = tk.OptionMenu(root, format_var, "mp4", "webm")
    format_option.pack()

    download_button = tk.Button(root, text="Download Video", command=start_download)
    download_button.pack()

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
    progress_bar.pack()

    root.mainloop()

parser = argparse.ArgumentParser(description='D3f4ults YouTube Video Downloader: Download videos from YouTube.')
parser.add_argument('--gui', action='store_true', help='Launch the graphical user interface.')
parser.add_argument('--url', type=str, help='YouTube video URL (for CLI mode).')
parser.add_argument('--path', type=str, help='Destination folder path (for CLI mode).')
parser.add_argument('--format', type=str, choices=['mp4', 'webm'], help='Video file format (for CLI mode).')

args = parser.parse_args()

if args.gui:
    gui_interface()
elif args.url and args.path and args.format:
    cli_interface(args.url, args.path, args.format)
else:
    parser.print_help()

import os
import shutil
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

def get_video_properties(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    return width, height, fps

def group_videos_by_properties_gui(source_folder):
    if not os.path.isdir(source_folder):
        messagebox.showerror("Error", "Invalid source folder.")
        return

    moved_files = 0
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.mp4'):
            video_path = os.path.join(source_folder, filename)
            props = get_video_properties(video_path)

            if props:
                width, height, fps = props
                folder_name = f"{width}x{height}_{fps}fps"
                target_folder = os.path.join(source_folder, folder_name)

                os.makedirs(target_folder, exist_ok=True)
                shutil.move(video_path, os.path.join(target_folder, filename))
                moved_files += 1

    messagebox.showinfo("Done", f"Organized {moved_files} video(s) by resolution and framerate.")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        group_videos_by_properties_gui(folder_selected)

# GUI Setup
app = tk.Tk()
#icon_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "packing.ico")
#app.iconbitmap(icon_path)
app.title("MP4 Video Organizer")
app.geometry("400x200")
app.resizable(False, False)

folder_path = tk.StringVar()

tk.Label(app, text="Select Source Folder", font=("Arial", 12)).pack(pady=10)
tk.Entry(app, textvariable=folder_path, width=50, state='readonly').pack(pady=5)
tk.Button(app, text="Browse", command=browse_folder, width=15).pack(pady=10)

tk.Label(app, text="Videos will be grouped into folders based on\nframe size and framerate.", font=("Arial", 10)).pack(pady=10)

app.mainloop()

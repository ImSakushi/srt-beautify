import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

def select_video_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.mkv *.mp4")])
    if file_paths:
        video_listbox.delete(0, tk.END)
        for file_path in file_paths:
            video_listbox.insert(tk.END, file_path)

def select_subtitle_file():
    file_path = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])
    if file_path:
        subtitle_entry.delete(0, tk.END)
        subtitle_entry.insert(0, file_path)

def run_processing():
    subtitle_path = subtitle_entry.get()
    language_code = language_combobox.get()
    videos = video_listbox.get(0, tk.END)

    if not videos:
        messagebox.showerror("Error", "Please select at least one video file.")
        return

    for video_path in videos:
        command = ['python', 'srtass.py', video_path, '-l', language_code]
        if subtitle_path:
            command.append(subtitle_path)

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to process {os.path.basename(video_path)}.\n{e}")
            break

# Création de la fenêtre principale
root = tk.Tk()
root.title("SRT to ASS Video Processor")

# Configuration du layout
video_frame = tk.Frame(root)
video_frame.pack(padx=20, pady=20)

video_listbox = tk.Listbox(video_frame, width=50, height=10)
video_listbox.pack(side=tk.LEFT)
video_scroll = tk.Scrollbar(video_frame, orient="vertical")
video_scroll.config(command=video_listbox.yview)
video_scroll.pack(side=tk.LEFT, fill=tk.Y)
video_listbox.config(yscrollcommand=video_scroll.set)

btn_select_video = tk.Button(root, text="Select Videos", command=select_video_files)
btn_select_video.pack(pady=(0, 20))

subtitle_frame = tk.Frame(root)
subtitle_frame.pack(padx=20, pady=20)
subtitle_entry = tk.Entry(subtitle_frame, width=50)
subtitle_entry.pack(side=tk.LEFT)
btn_select_subtitle = tk.Button(subtitle_frame, text="Select Subtitle", command=select_subtitle_file)
btn_select_subtitle.pack(side=tk.LEFT, padx=(10,0))

# ComboBox pour sélectionner la langue
language_label = tk.Label(root, text="Select Subtitle Language:")
language_label.pack()
language_combobox = ttk.Combobox(root, values=[
    "fre", "eng", "spa", "ger", "ita", "por", "rus", "jpn", "kor", "chi", "ara"
])
language_combobox.set("fre")  # Définir une valeur par défaut
language_combobox.pack()

btn_run = tk.Button(root, text="Process Videos", command=run_processing)
btn_run.pack(pady=(0, 20))

root.mainloop()

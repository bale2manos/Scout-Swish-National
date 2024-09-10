import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from code.media.process_image import process_images
from code.media.image_to_text import get_player_name
from code.media.cropping import crop_image_to_second_third_row, crop_image_to_second_fifth_row
from code.devices.windows import screenshot_window_by_title
from utils.utils import remove_temp_images


def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_selected)


def toggle_advanced_mode():
    if advanced_mode_var.get():
        root.geometry(f"{window_width}x{window_height + 180}+{x_cordinate}+{y_cordinate}")
        window_title_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='ew')
        tesseract_path_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='ew')
        advanced_button.config(text="Hide Advanced Mode")
    else:
        window_title_frame.grid_forget()
        tesseract_path_frame.grid_forget()
        root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        advanced_button.config(text="Show Advanced Mode")

    root.update_idletasks()
    start_button.grid(row=6 if advanced_mode_var.get() else 4, column=0, columnspan=3, pady=20)


def show_error(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("400x150")
    error_window.configure(background='#F8D7DA')

    message_label = ttk.Label(error_window, text=message, font=('Helvetica', 12), foreground='#721C24', background='#F8D7DA', wraplength=360)
    message_label.pack(pady=20, padx=20, fill='x', expand=True)

    ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(pady=10)

    message_label.update_idletasks()


def start_process():
    folder_path = folder_path_entry.get()
    n_games_str = n_games_entry.get()
    window_title = window_title_entry.get() if advanced_mode_var.get() else "BlueStacks App Player"
    tesseract_path = tesseract_path_entry.get() if advanced_mode_var.get() else "F:/Programas/Tesseract-OCR/tesseract.exe"

    # Validate inputs
    if not folder_path:
        show_error("Folder path cannot be empty.")
        return

    if not n_games_str.isdigit() or int(n_games_str) < 1:
        show_error("Number of games must be a number greater than 0.")
        return

    n_games = int(n_games_str)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create necessary directories
    if not os.path.exists(f'{folder_path}/Stats Cropped'):
        os.makedirs(f'{folder_path}/Stats Cropped')

    if not os.path.exists(f'{folder_path}/Results'):
        os.makedirs(f'{folder_path}/Results')

    # Take screenshot
    screenshot_window_by_title(window_title, n_games, folder_path, tesseract_path)

    # Remove all images from the folder starting with 'temp'
    remove_temp_images(folder_path)

    messagebox.showinfo("Process Completed", "The process has been completed successfully.")


# Create main window
root = tk.Tk()
root.title("Basketball Stats Processor")

# Set initial window size and center it on the screen
window_width = 900
window_height = 460  # Adjusted height to include n_games field
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.configure(background='#F5F5F5')

style = ttk.Style()
style.configure("TLabel", background='#F5F5F5', foreground='#333333', font=('Helvetica', 14))
style.configure("TEntry", padding=5, font=('Helvetica', 12))
style.configure("TButton", background='#141414', foreground='#141414', font=('Helvetica', 12, 'bold'), padding=10)
style.map("TButton", background=[('active', '#444444')])
style.configure("TFrame", background='#F5F5F5')

title_label = ttk.Label(root, text="🏀 Basketball Stats Processor 🏀", font=('Helvetica', 20, 'bold'))
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Folder path
folder_path_label = ttk.Label(root, text="Select Folder:")
folder_path_label.grid(row=1, column=0, padx=20, pady=10)
folder_path_entry = ttk.Entry(root, width=50)
folder_path_entry.grid(row=1, column=1, padx=20, pady=10)
browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=20, pady=10)

# Number of games
n_games_label = ttk.Label(root, text="Number of Games:")
n_games_label.grid(row=2, column=0, padx=20, pady=10)
n_games_entry = ttk.Entry(root, width=10)
n_games_entry.grid(row=2, column=1, padx=20, pady=10)

# Advanced mode button
advanced_mode_var = tk.BooleanVar(value=False)
advanced_button = ttk.Button(root, text="Show Advanced Mode", command=lambda: advanced_mode_var.set(not advanced_mode_var.get()) or toggle_advanced_mode())
advanced_button.grid(row=3, column=0, columnspan=3, pady=10)

# Window Title Frame
window_title_frame = ttk.Frame(root)
window_title_label = ttk.Label(window_title_frame, text="Window Title:")
window_title_label.grid(row=0, column=0, padx=20, pady=10)
window_title_entry = ttk.Entry(window_title_frame, width=50)
window_title_entry.grid(row=0, column=1, padx=20, pady=10)
window_title_entry.insert(0, "BlueStacks App Player")

# Tesseract Path Frame
tesseract_path_frame = ttk.Frame(root)
tesseract_path_label = ttk.Label(tesseract_path_frame, text="Tesseract Path:")
tesseract_path_label.grid(row=0, column=0, padx=20, pady=10)
tesseract_path_entry = ttk.Entry(tesseract_path_frame, width=50)
tesseract_path_entry.grid(row=0, column=1, padx=20, pady=10)
tesseract_path_entry.insert(0, r'F:/Programas/Tesseract-OCR/tesseract.exe')

# Start button
start_button = ttk.Button(root, text="Start Process", command=start_process)
start_button.grid(row=4, column=0, columnspan=3, pady=20)

root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Main loop
root.mainloop()

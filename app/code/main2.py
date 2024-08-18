import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from code.media.process_image import process_images
from code.media.image_to_text import get_player_name
from code.media.cropping import crop_image_to_second_third_row, crop_image_to_second_fifth_row
from code.devices.windows import screenshot_window_by_title

def start_process():
    folder_path = 'F:/PyCharm/scout-swish/Scout-Swish-National/teams/Villa'
    n_games = 2
    window_title = "BlueStacks App Player"
    tesseract_path = "F:/Programas/Tesseract-OCR/tesseract.exe"

    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create necessary directories
    if not os.path.exists(f'{folder_path}/Stats Cropped'):
        os.makedirs(f'{folder_path}/Stats Cropped')

    if not os.path.exists(f'{folder_path}/Results'):
        os.makedirs(f'{folder_path}/Results')

    # Take screenshot
    screenshot_window_by_title(window_title, n_games, folder_path, tesseract_path)


    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'GENERAL_STATS_temp.png':
            image_path = os.path.join(folder_path, filename)
            try:
                player_name = get_player_name(image_path, f'{folder_path}/temp.png', tesseract_path)
                player_stats_output_path = f'{folder_path}/Stats Cropped/{player_name}.png'
                crop_image_to_second_third_row(image_path, player_stats_output_path)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")


    messagebox.showinfo("Process Completed", "The process has been completed successfully.")


start_process()
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from code.media.process_image import process_images
from code.media.image_to_text import get_player_name
from code.media.cropping import crop_image_to_second_third_row, crop_image_to_second_fifth_row
from code.devices.windows import screenshot_window_by_title
from utils.utils import remove_temp_images


def start_process():
    folder_path = 'F:/PyCharm/scout-swish/Scout-Swish-National/teams/Pintobasket'
    n_games = 10
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

    # Remove all images from the folder starting with 'temp'
    remove_temp_images(folder_path)


    messagebox.showinfo("Process Completed", "The process has been completed successfully.")


start_process()
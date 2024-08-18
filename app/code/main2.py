import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from code.media.process_image import process_images, get_team_stats
from code.media.image_to_text import get_player_name
from code.media.cropping import crop_image_to_second_third_row, crop_image_to_second_fifth_row
from code.devices.windows import screenshot_window_by_title

def start_process():
    folder_path = 'F:/PyCharm/scout-swish/Scout-Swish-National/teams/Villa'
    n_players = 2
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
    screenshot_window_by_title(window_title, n_players, folder_path, tesseract_path)



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

    # Process general stats and save
    crop_image_to_second_fifth_row(f'{folder_path}/GENERAL_STATS_temp.png', f'{folder_path}/Stats Cropped/GENERAL_STATS.png')
    team_stats = get_team_stats(f'{folder_path}/Stats Cropped/GENERAL_STATS.png')

    with open(f'{folder_path}/Results/Team Stats.txt', 'w') as f:
        for key, value in team_stats.items():
            f.write(f"{key}: {value}\n")

    process_images(f'{folder_path}/Stats Cropped', f'{folder_path}/Results/Players Stats.xlsx')

    messagebox.showinfo("Process Completed", "The process has been completed successfully.")


start_process()
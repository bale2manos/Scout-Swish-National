import os

from ..data.excel import save_to_excel
from ..data.text_to_data import extract_player_name, extract_data_from_text
from ..media.image_to_text import extract_numbers
from ..media.preprocess_image import preprocess_image_adding_rectangles, preprocess_image


def process_images(folder_path, excel_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'GENERAL_STATS.png':
            image_path = os.path.join(folder_path, filename)
            try:
                print(f"Processing {image_path}...")
                preprocessed_image = preprocess_image_adding_rectangles(image_path)
                text = ''
                #text = extract_numbers(preprocessed_image)
                player_name = extract_player_name(filename)
                player_data = extract_data_from_text(text, player_name)
                if player_data:
                    data.append(player_data)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    save_to_excel(data, excel_path)

import cv2
import numpy as np
from PIL import Image
import pytesseract
import os

from utils.bucket import change_color
from ..utils.bucket import bucket_fill
from .preprocess_image import preprocess_image, read_image, resize_image, save_image, invert_colors, apply_threshold, \
    enhance_image, sharpen_image
from ..media.cropping import crop_image_to_top, crop_players_names, crop_stats, crop_player_numbers
from ..utils.utils import remove_initial_wrong_chars




def read_text_from_image(image_path, tesseract_cmd_path):
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    # Open the image file
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img, lang='spa')
        print(f"Extracted text: {text}")
        # Remove any leading or trailing whitespace
        text = text.strip()

    # Capitalize the first letter of each word
    text = text.title()

    # Remove the image file
    os.remove(image_path)

    return text


def get_player_name(image_path,output_path, tesseract_cmd_path):
    crop_image_to_top(image_path, output_path)
    return read_text_from_image(output_path, tesseract_cmd_path)


def extract_numbers(image):
    image_pil = Image.fromarray(image)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789.:%-'

    extracted_text = pytesseract.image_to_string(image_pil, config=custom_config)
    print(f"Extracted text: {extracted_text}")
    return extracted_text

def get_team_names(image_path, tesseract_cmd_path):
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    # Open the image file
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img, lang='spa')
        print(f"Extracted text: {text}")
        # Remove any leading or trailing whitespace
        text = text.strip()

    #text = remove_initial_wrong_chars(text)

    # Remove any leading or trailing whitespace
    text = text.strip()

    # Capitalize the first letter of each word
    text = text.title()

    # Remove the image file
    #os.remove(image_path)

    teams = text.split('\n')
    # Remove empty strings
    teams = list(filter(None, teams))

    # Maximum of 2 teams
    if len(teams) > 2:
        teams = teams[:2]

    return teams

def get_players_names(image_path, tesseract_cmd_path):
    # First crop the image to just get the numbers
    names_path = crop_players_names(image_path)

    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    text = read_text_from_image(names_path, tesseract_cmd_path)

    # Split the text into lines
    names = text.split('\n')
    # Remove empty strings
    names = list(filter(None, names))

    # If one cell contains just one word, add that word to the previous cell and remove the empty cell
    i = 1
    while i < len(names):
        if len(names[i].split()) == 1:
            names[i-1] = names[i-1] + " " + names[i]
            names.pop(i)
        elif len(names[i].split()) == 2 and (names[i].split()[0] == 'De' or names[i].split()[0] == 'Del'):
            names[i-1] = names[i-1] + " " + names[i]
            names.pop(i)
        elif '...' in names[i]:
            names[i-1] = names[i-1] + " " + names[i]
            names.pop(i)
        i += 1


    return names

def get_team_stats(image_path, tesseract_cmd_path):
    # First crop the image to just get the numbers
    stats_path = crop_stats(image_path)

    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    # Read the numbers from the image
    text = extract_numbers_from_path(stats_path)
    print(f"Extracted stats: {text}")

    # Split the text into lines
    text = text.split('\n')

    print(f"Extracted stats after splitting: {text}")

    # Remove empty strings
    text = list(filter(None, text))

    # For each element, split by spaces so that stats are in a list of lists
    stats = [line.split() for line in text]

    print("Stats: ", stats)

    return stats

def extract_numbers_from_path(image_path):
    image = read_image(image_path)
    inverted_image = invert_colors(image)
    scaled_image = resize_image(inverted_image)

    save_image(scaled_image, './numbers_image.png')
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.:%-/'

    extracted_text = pytesseract.image_to_string(inverted_image, config=custom_config)
    print(f"Extracted text: {extracted_text}")

    os.remove('./numbers_image.png')

    return extracted_text

def get_players_numbers(image_path, tesseract_cmd_path, local_away):
    if local_away == 0:
        team_color = (107,107,107)
        tolerance_team = 90
        tolerance_color_replace = 70
    else:
        team_color = (166, 166, 166)
        tolerance_team = 70
        tolerance_color_replace = 60

    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    # Crop the image
    cropped_path = crop_player_numbers(image_path)

    # Read the image
    image = read_image(cropped_path)

    # Invert colors
    inverted_image = invert_colors(image)

    # Optionally resize image
    scaled_image = resize_image(inverted_image)

    # Save the processed image
    processed_image_path = './processed_image.png'
    save_image(scaled_image, processed_image_path)

    # Bucket of gray paint to paint the image
    bucket_path = bucket_fill(processed_image_path,10, 10, team_color, tolerance=tolerance_team)

    # Change the image gray to black
    final_path = change_color(bucket_path, team_color, (0,0,0), tolerance=tolerance_color_replace)

    # Configure Tesseract to only recognize digits (0-9)
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'

    # Read the numbers from the image
    extracted_text = pytesseract.image_to_string(final_path, config=custom_config)
    print(f"Extracted text: {extracted_text.strip()}")

    # Remove all images generated besides the original image

    os.remove(cropped_path)
    os.remove(processed_image_path)
    os.remove(bucket_path)
    os.remove(final_path)



    # Split the text into lines
    extracted_text = extracted_text.split('\n')
    # Remove empty strings
    extracted_text = list(filter(None, extracted_text))

    return extracted_text








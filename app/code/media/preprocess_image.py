import os

import cv2
import numpy as np

from ..utils.utils import create_temp_copy


def preprocess_image_adding_rectangles(image_path):
    temp_path = create_temp_copy(image_path)

    image = read_image(temp_path)

    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {temp_path}. Please ensure the file exists and is accessible.")

    # Define rectangle properties
    # First rectangle goes full width from 0% to 20% of the height
    rect1_top_left = (0, 0)
    rect1_bottom_right = (image.shape[1], 38 * image.shape[0] // 100)

    # Rectange in the furthest left column (10% width) from 0% to 100% of the height
    rect2_top_left = (85 * image.shape[1] // 100, 0)
    rect2_bottom_right = (image.shape[1], image.shape[0])

    rects = [(rect1_top_left, rect1_bottom_right), (rect2_top_left, rect2_bottom_right)]


    # Draw rectangles on the image
    for (top_left, bottom_right) in rects:
        cv2.rectangle(image, top_left, bottom_right, 255, thickness=cv2.FILLED)

    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)

    # Resize for better OCR accuracy
    scaled_image = resize_image(inverted_image)

    # Save the image
    cv2.imwrite(temp_path, scaled_image)
    print(f"Preprocessed image saved to {temp_path}")

    return temp_path


def read_image(temp_path):
    # Read the image in grayscale from the new path
    image = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
    return image


def preprocess_image(image_path):
    # Read the image in grayscale from the new path
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {image_path}. Please ensure the file exists and is accessible.")
    # Invert colors if needed
    #inverted_image = cv2.bitwise_not(image)
    scaled_image = resize_image(image)

    # Save the image
    cv2.imwrite("./numbers_image.png", scaled_image)
    return scaled_image


def resize_image(image):
    # Resize for better OCR accuracy
    scaled_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return scaled_image

def save_image(image, output_path):
    cv2.imwrite(output_path, image)
    print(f"Image saved to {output_path}")

def invert_colors(image):
    return cv2.bitwise_not(image)

def apply_threshold(image):
    _, thresh_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return thresh_image

def enhance_image(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.dilate(image, kernel, iterations=1)
    processed_image = cv2.erode(processed_image, kernel, iterations=1)
    return processed_image

def sharpen_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  # sharpening kernel
    return cv2.filter2D(image, -1, kernel)

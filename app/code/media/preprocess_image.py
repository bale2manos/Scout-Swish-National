import os

import cv2

from ..utils.utils import create_temp_copy


def preprocess_image_adding_rectangles(image_path):
    temp_path = create_temp_copy(image_path)

    # Read the image in grayscale from the new path
    image = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)

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
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Save the image
    cv2.imwrite(temp_path, scaled_image)
    print(f"Preprocessed image saved to {temp_path}")

    # Optionally remove the temporary file if you no longer need it
    #os.remove(temp_path)


    return scaled_image


def preprocess_image(image_path):
    # Read the image in grayscale from the new path
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {image_path}. Please ensure the file exists and is accessible.")
    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)
    # Resize for better OCR accuracy
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return scaled_image

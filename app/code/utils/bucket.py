from PIL import Image


def bucket_fill(image_path, start_x, start_y, new_color, tolerance=50):
    """
    Fill all adjacent pixels similar to the starting pixel's color with new_color.

    :param image_path: Path to the image file.
    :param start_x: X coordinate of the starting pixel.
    :param start_y: Y coordinate of the starting pixel.
    :param new_color: New color to fill with, should be an (R, G, B) tuple.
    :param tolerance: Tolerance level for color similarity (0-255). Higher value means more tolerance.
    :return: Path to the saved filled image.
    """

    # Open the image
    image = Image.open(image_path)

    # Ensure the image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels = image.load()  # Create a pixel map

    # Get the color of the starting pixel
    start_color = pixels[start_x, start_y]

    def color_difference(c1, c2):
        """Calculate the difference between two colors."""
        return sum(abs(a - b) for a, b in zip(c1, c2))

    def is_similar(color1, color2, tolerance):
        """Check if two colors are similar within a tolerance."""
        return color_difference(color1, color2) <= tolerance * 3

    # Define a function for checking if a pixel is within image bounds
    def is_within_bounds(x, y):
        return 0 <= x < image.width and 0 <= y < image.height

    # Define a function to perform the flood fill
    def flood_fill(x, y):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if is_within_bounds(x, y) and is_similar(pixels[x, y], start_color, tolerance):
                pixels[x, y] = new_color
                # Add neighboring pixels to the stack
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

    # Perform the flood fill
    flood_fill(start_x, start_y)

    # Save the result to a new file
    filename_without_extension = image_path.rsplit('.', 1)[0]
    result_path = f"{filename_without_extension}_filled.png"
    image.save(result_path)
    return result_path


def change_color(image_path, tuple_origin, tuple_changed, tolerance=70):
    """
    Change all pixels of a specific color (tuple_origin) to another color (tuple_changed)
    within a specified tolerance.

    :param image_path: Path to the image file.
    :param tuple_origin: The color to be replaced (R, G, B) tuple.
    :param tuple_changed: The new color to use (R, G, B) tuple.
    :param tolerance: Tolerance level for color similarity (0-255). Higher value means more tolerance.
    :return: Path to the saved updated image.
    """

    def color_difference(c1, c2):
        """Calculate the difference between two colors."""
        return sum(abs(a - b) for a, b in zip(c1, c2))

    def is_similar(color1, color2, tolerance):
        """Check if two colors are similar within a tolerance."""
        return color_difference(color1, color2) <= tolerance * 3

    # Open the image
    image = Image.open(image_path)
    original_mode = image.mode

    # Ensure the image is in a mode that can handle color changes
    if original_mode not in ['RGB', 'RGBA', 'P']:
        raise ValueError("Unsupported image mode for color change. Use RGB, RGBA, or P.")

    pixels = image.load()  # Create a pixel map

    def is_target_color(color):
        """Check if the pixel color is within tolerance of the origin color."""
        if original_mode == 'P':
            # Handle palette images
            palette = image.getpalette()
            color_rgb = palette[color * 3:color * 3 + 3]
            return is_similar(color_rgb, tuple_origin, tolerance)
        elif original_mode == 'RGBA':
            return is_similar(color[:3], tuple_origin, tolerance)  # Ignore alpha channel
        else:
            return is_similar(color, tuple_origin, tolerance)

    def set_new_color(x, y):
        """Set the new color at pixel (x, y)."""
        if original_mode == 'P':
            # Find the closest palette index for the new color
            palette = image.getpalette()
            closest_index = min(range(len(palette)//3), key=lambda i: color_difference(palette[i*3:i*3+3], tuple_changed))
            pixels[x, y] = closest_index
        elif original_mode == 'RGBA':
            pixels[x, y] = tuple_changed + (pixels[x, y][3],)  # Preserve alpha channel
        else:
            pixels[x, y] = tuple_changed

    # Iterate through all pixels and change color if it matches the target within tolerance
    for x in range(image.width):
        for y in range(image.height):
            if is_target_color(pixels[x, y]):
                set_new_color(x, y)

    # Save the result to a new file
    filename_without_extension = image_path.rsplit('.', 1)[0]
    result_path = f"{filename_without_extension}_color_changed.png"
    image.save(result_path)
    return result_path


from math import sqrt
import os
import json
from PIL import Image
from constants.rgb_definitions import ARROW_RGB

# Constants for bounding box adjustments
BOX_HEIGHT_UP = 75
BOX_HEIGHT_DOWN = 50
BOX_WIDTH_LEFT = 100
BOX_WIDTH_RIGHT = 25


def look_for_arrow(image, text_coords):
    """
    Detect the arrow direction and its head based on the bounding box and ARROW_RGB.
    """
    x_center, y_center = map(float, text_coords[:2])

    # Define the bounding box around "to"
    x_min = x_center - BOX_WIDTH_LEFT
    x_max = x_center + BOX_WIDTH_RIGHT
    y_min = y_center - BOX_HEIGHT_UP
    y_max = y_center + BOX_HEIGHT_DOWN
    
    bbox_width = x_max - x_min
    image_width = image.size[0]

    # Start with a bounding box around the text and extend it to the left and right
    # if pixel seen to left, direction is left, if pixel seen to right, direction is right
    direction_found = None
    for direction in ['left', 'right']:
        offset = 0
        while offset < 0.2 * image_width:  # Stop after covering 20% of the image width
            if direction == 'left':
                x_max_check = x_min_check if 'x_min_check' in locals() else x_max
                x_min_check = max(0, x_min - offset)
            else:
                x_min_check = x_max_check if 'x_max_check' in locals() else x_min
                x_max_check = min(image_width, x_max + offset)

            # Create the bounding box
            bbox = (int(x_min_check), int(y_min), int(x_max_check), int(y_max))
            cropped = image.crop(bbox)
            cropped_data = list(cropped.getdata())

            # Check for ARROW_RGB in the bounding box
            arrow_pixels = [pixel for pixel in cropped_data if pixel in ARROW_RGB]
            if arrow_pixels:
                direction_found = direction
                break
            offset += bbox_width
        if direction_found:
            break

    return direction_found

def look_for_train(image, text_coords):
    
    arrow_direction = look_for_arrow(image, text_coords)
    # Get full image dimensions.
    width, height = image.size

    offset_x = 650
    # Crop the image so that the x-coordinate starts at 650.
    cropped = image.crop((offset_x, 0, width, height))
    cropped_width, _ = cropped.size

    # Adjust the text x coordinate relative to the cropped image.
    text_x = float(text_coords[0]) - 650
    # Define the midpoint of the cropped image.
    midpoint = cropped_width / 2
    dist = abs(text_x - midpoint)

    # Decide the relative position of the text.
    if midpoint - 200 <= text_x <= midpoint + 200:
        pos = "middle"
    elif text_x < midpoint - 200:
        pos = "left"
    else:
        pos = "right"

    train_coords = {1:offset_x + cropped_width/2}


    if arrow_direction == 'left':
        if pos == "left":
            train_coords[0] = offset_x + text_x
            train_coords[2] = offset_x + midpoint + dist
        else:
            train_coords[2] = offset_x + text_x
            train_coords[0] = offset_x + midpoint + dist
    else:
        if pos == "right":
            train_coords[2] = offset_x + text_x
            train_coords[0] = offset_x + midpoint + dist
        else:
            train_coords[0] = offset_x + text_x
            train_coords[2] = offset_x + midpoint + dist
    
    return train_coords

def determine_direction():
    for station in os.listdir('station_data_json'):
        station_path = os.path.join('station_data_json', station)
        with open(station_path, 'r') as file:
            data = json.load(file)

        image_path = f"stations_png/{station.replace('.json', '.png')}"  # Assuming corresponding image files are in station_images
        if not os.path.exists(image_path):
            continue

        image = Image.open(image_path)
        image = image.convert('RGB')
        transformed_data = {}
        for line, coords in data.items():
            if len(coords) < 2:
                continue  # Skip invalid entries
            # Determine train location
            train_location = look_for_train(image, coords)
            # Sort the keys before placing them
            sorted_train_location = {k: train_location[k] for k in sorted(train_location)}
            transformed_data[line] = sorted_train_location

        # Overwrite the file with transformed data
        with open(station_path, 'w') as file:
            json.dump(transformed_data, file, indent=4)

        print(f"Processed {station}")
import os
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
from constants.rgb_definitions import OUTER_RGB, INNER_RGB
from utils.exit_coords import save_exits_data

def find_exit_coordinates(image):
    height = len(image)
    width = len(image[0])
    exits = []
    for y in range(height):
        for x in range(width):
            if image[y][x] in OUTER_RGB and not any(
                exit[0] <= x < exit[0] + exit[2] and exit[1] <= y < exit[1] + exit[2] for exit in exits
            ):
                size = 1
                while (
                    x + size < width
                    and y + size < height
                    and image[y][x + size] in OUTER_RGB
                    and image[y + size][x] in OUTER_RGB
                ):
                    size += 1

                if (
                    size > 1
                    and y + size + 1 < height
                    and x + size + 1 < width
                    and image[y + size + 1][x] not in OUTER_RGB
                    and image[y][x + size + 1] not in OUTER_RGB
                ):
                    # Check if INNER_RGB are found inside the region
                    inner_found = False
                    for inner_y in range(y + 1, y + size - 1):
                        for inner_x in range(x + 1, x + size - 1):
                            if image[inner_y][inner_x] in INNER_RGB:
                                inner_found = True
                                break
                        if inner_found:
                            break

                    if inner_found:
                        exits.append((x, y, size))
    return exits


def enhance_contrast(image):
    # Automatically adjust contrast
    image = ImageOps.autocontrast(image, cutoff=2)
    # Further enhance contrast manually
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)  # Increase contrast by 3x
    return image

def preprocess_image(image):
    # Grayscale the image
    image = ImageOps.grayscale(image)   
    # Enhance contrast
    image = enhance_contrast(image)

    return image

def extract_text_from_exit(image, coordinates):
    """
    Extract text from the detected exits using OCR.
    """
    exits_coordinates = dict()

    for i, (x, y, size) in enumerate(coordinates):
        # Crop the region of interest
        cropped_region = [row[x:x + size] for row in image[y:y + size]]
        cropped_image = Image.new('RGB', (size, size))
        for j, row in enumerate(cropped_region):
            for i, pixel in enumerate(row):
                cropped_image.putpixel((i, j), pixel)
        
        # Preprocess the cropped region for OCR
        preprocessed_image = preprocess_image(cropped_image)
        
        # Perform OCR
        text = pytesseract.image_to_string(
                preprocessed_image,
                config='--oem 1 --psm 7 -c tessedit_char_whitelist=ABCDEFGHJKLMNPR123456' # configure OCR to look in this range only
            )
        
        text = text.strip()
        if len(text) == 0:
            text = str(i)

        if text not in exits_coordinates.keys():
            exits_coordinates[text] = [x+size//2, y+size//2]
        else:
            exits_coordinates[text[0]+str(i)] = [x+size//2, y+size//2]
    
    return exits_coordinates
      

# main function to extract exits
def extract_exits():
    # Tesseract OCR path setup
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    exits_data = dict()
    for image_path in os.listdir('stations_png'):
        print("Getting exit coordinates for station:", image_path + "...")
        # Load image
        image_path = os.path.join('stations_png', image_path)
        image = Image.open(image_path)
        image = image.convert('RGB')
        
        # Convert the image into a 2D list of RGB tuples
        width, height = image.size
        image_data = list(image.getdata())
        image_data = [image_data[i * width:(i + 1) * width] for i in range(height)]
        
        # skip the header in the image containing OUTER_RGB
        i = 0
        while i < len(image_data) and image_data[i][0] in OUTER_RGB:
            i += 1
        
        # Crop the image to exclude the top rows with OUTER_RGB
        cropped_image_data = image_data[i:]
        
        # Find exit coordinates
        coordinates = find_exit_coordinates(cropped_image_data)
        
        # adjust cropped coordinates to original image coordinates
        coordinates = [(x, y + i, size) for (x, y, size) in coordinates]
        
        # Extract text from each exit
        exits_data[image_path[13:-4]] = extract_text_from_exit(image_data, coordinates)


    # Save the exits data
    print("Saving exits coordinates data...")
    save_exits_data(exits_data)


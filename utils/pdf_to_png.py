from ironpdf import *
import os
from constants.directory_names import DIRECTORY_NAMES

def convertToPNG(dpi = 250):
    directory = f"{os.getcwd()}\\{DIRECTORY_NAMES["STATION_PNGs_" + str(dpi)]}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    error_files = []
    directory = DIRECTORY_NAMES["STATION_PNGs_" + str(dpi)] + "\\"
    for filename in os.listdir(DIRECTORY_NAMES["STATION_PDFs"]):
        print("Converting ",filename,"to png....")
        try:
            pdf = PdfDocument.FromFile(f"{DIRECTORY_NAMES["STATION_PDFs"]}\\{filename}")
            pdf.RasterizeToImageFiles(directory + filename[:-4] + '.png', DPI=dpi)
        except:
            error_files.append(filename)
    
    if error_files:
        print(f"Error converting the following files to PNG (dpi={dpi}):")
        print("\n".join(error_files))
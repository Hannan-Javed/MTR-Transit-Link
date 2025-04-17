import shutil
from constants.directory_names import DIRECTORY_NAMES
from utils.pdf_to_png import convertToPNG
from utils.webcrawler import downloadStationLayouts
import ocr.compartments_ocr as compartments_ocr
import ocr.exits_ocr as exits_ocr
import ocr.google_vision.lines_ocr as lines_ocr
from utils.clean_data.exit_coords import clean_exits_data
from utils.clean_data.station_coords import clean_station_lines_data
from utils.determine_closest_compartment import process_exit_and_station_data

if __name__ == "__main__":

    # First download the station layouts
    print("Downloading Station Layouts.....")
    downloadStationLayouts()

    # Convert the downloaded PDFs to PNG format for OCR
    convertToPNG()
    
    print("Performing OCR......")

    # Perform OCR on the train lines
    lines_ocr.OCR()

    # Clean the data obtained and convert to json format
    clean_station_lines_data()

    # perform OCR to determine compartments location for trains
    compartments_ocr.OCR()

    # convert to higher dpi for exits
    convertToPNG(dpi=1000)

    # Perform OCR to determine exits location for stations
    exits_ocr.OCR()

    # Final step - determine the closest compartment for each exit    
    process_exit_and_station_data('exits_data_json', 'station_data_json', 'closest_compartments')

    # Delete all the temporary files created during the process
    import shutil
    for key, directory in DIRECTORY_NAMES.items():
        if key != "FINAL_OUTPUT":
            shutil.rmtree(directory, ignore_errors=True)

    


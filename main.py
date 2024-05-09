from webcrawler import downloadStationLayouts
from pdf_to_png import convertToPNG
from google_vision import linesocr

if __name__ == "__main__":
    

    print("Downloading Station Layouts.....")
    # First download the station layouts
    downloadStationLayouts()
    print("Covnerting to PNG format for OCR......")
    # Create another directory to convert and save pngs for google ocr
    convertToPNG()
    print("Performing OCR on stations and lines....")
    # perform OCR
    linesocr.OCR()
    

    


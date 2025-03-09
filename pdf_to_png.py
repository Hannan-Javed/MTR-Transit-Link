from ironpdf import *
import os


def convertToPNG():

    if not os.path.exists(os.getcwd() + "\\stations_png"):
        os.makedirs(os.getcwd() + "\\stations_png")
    error_files = []
    for filename in os.listdir(os.getcwd()+"\\stations"):
        print("Converting ",filename,"to png....")
        try:
            pdf = PdfDocument.FromFile(os.getcwd()+"\\stations\\"+filename)
            pdf.RasterizeToImageFiles("stations_png/"+filename[:-4]+'.png',DPI=1000)
        except:
            error_files.append(filename)
    
    if error_files:
        print("Error converting the following files:")
        for file in error_files:
            print(file)

convertToPNG()
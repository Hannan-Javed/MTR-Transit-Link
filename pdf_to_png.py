from ironpdf import *
import os


def convertToPNG():
    if not os.path.exists(os.getcwd() + "\\stations_png"):
        os.makedirs(os.getcwd() + "\\stations_png")
    for filename in os.listdir(os.getcwd()+"\\stations"):
        print("Converting ",filename,"to png....")
        pdf = PdfDocument.FromFile(os.getcwd()+"\\stations\\"+filename)
        pdf.RasterizeToImageFiles("stations_png/"+filename[:-4]+'.png',DPI=250)

    print("Conversion complete")

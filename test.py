import ironpdf, os

pdf = ironpdf.PdfDocument.FromFile(os.getcwd()+"\\stations\\Admiralty.pdf")
pdf.RasterizeToImageFiles("stations_png/Admiralty.png",DPI=500)
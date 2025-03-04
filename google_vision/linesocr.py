import io
import os
from google.cloud import vision

def savestationdata(stationname, linescoordinates):

    file = open(os.getcwd()+"\\stationdata\\"+stationname+".txt",'w',encoding="utf-8")
    for lines, coordinates in linescoordinates.items():
        print(lines+": "+" ; ".join(coordinates))
        file.write(lines+": "+" ; ".join(coordinates)+'\n')
    file.close()

def OCR():
    os.environ['GOOGLE_APPLICTION_CREDENTIALS'] = 'client_file.json'
    client = vision.ImageAnnotatorClient()

    directory = os.getcwd() + "\\stationdata"

    if not os.path.exists(directory):
        os.makedirs(directory)
        
    for imgfile in os.listdir(os.getcwd()+"\\stations_png"):
        print(imgfile, end='')
        with io.open(os.getcwd()+"\\stations_png\\"+imgfile, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content = content)

        response = client.text_detection(image = image)
        texts = response.text_annotations
        print("Texts:")

        Line = []
        Lines = {}

        check = False

        for text in texts:
            
            Line.append(text.description)

            if text.description == "to":
                check = True
                Line.pop(0)
                continue

            # most stations have only one end line
            if text.description == "End":
                vertices = [
                f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
                ]
                if " ".join(Line) not in Lines:
                    Lines[" ".join(Line[-1])] = [(",".join(vertices))]
                else:
                    Lines[" ".join(Line[-1])] = Lines[" ".join(Line)] + [(",".join(vertices))]
                Line.pop(0)
                continue

            if check:
                vertices = [
                f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
                ]
                if " ".join(Line) not in Lines:
                    Lines[" ".join(Line)] = [(",".join(vertices))]
                else:
                    Lines[" ".join(Line)] = Lines[" ".join(Line)] + [(",".join(vertices))]
                
                check = False
                Line = []
                

            if len(Line)>4:
                Line.pop(0)


        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
        
OCR()

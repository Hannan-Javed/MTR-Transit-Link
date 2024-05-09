import cv2, os
import numpy as np  

for stations in os.listdir("stations_png\\"):
    station = cv2.imread("stations_png\\"+stations)   
    for exits in os.listdir("exits\\"):
        exit = cv2.imread("exits\\"+exits)  
        result = cv2.matchTemplate(station, exit, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        max_index = np.unravel_index(result.argmax(), result.shape)
        swapped_index = (max_index[1], max_index[0])  # Swapping the row and column indices
        print(stations, exits, min_val, max_val, min_loc, max_loc, swapped_index)
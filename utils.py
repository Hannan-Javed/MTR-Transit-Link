import os, re
import json
LINE_CONVERSION = {
    "Kwan O Line": "Tseung Kwan O Line",
}
STATION_CONVERSION = {
    "Kennedy": "Kennedy Town",
    "South": "South Horizons",
    "Tsuen": "Tsuen Wan",
    "Lo": "Lo Wu",
    "Chai": "Chai Wan",
    "Asia": "AsiaWorld-Expo",
    "Tuen": "Tuen Mun",
    "Wu": "Wu Kai Sha",
    "Tiu": "Tiu Keng Leng",
    "Sunny": "Sunny Bay",
    "Po": "Po Lam",
    "North": "North Point",
    "Tung": "Tung Chung",
    "機場 博覽 館": "AsiaWorld-Expo",
    "or": "AsiaWorld-Expo",
    "Hung": "Hung Hom",
    "Disneyland": "Disneyland Resort",
}
END_CONVERSION = {
    "Admiralty": "East Rail Line",
    "Kennedy Town": "Island Line",
    "North Point": "Island Line",
    "Tiu Keng Leng": "Tseung Kwan O Line",
    "Tsuen Wan": "Tsuen Wan Line",
}
def clean_data():
    os.makedirs('station_data_json', exist_ok=True)
    for file in os.listdir('stationdata'):
        with open('stationdata/'+file, 'r', encoding='utf-8') as f:
            data = f.read()
            converted = ''
            for file_line in data.split('\n'):
                if "E n d" not in file_line and ("to" not in file_line or "concourse" in file_line.lower()):
                    continue
                direc, coordinates = file_line.split(': ')
                direc = ''.join(filter(lambda x: re.match(r'[A-Za-z\s ]', x), direc)).strip()
                if direc == "E n d":
                    converted += "End of the " + END_CONVERSION[file[:-4]] + ': '
                else:
                    keyword_found = next((keyword for keyword in ['city', 'AsiaWorld', 'Airport', 'to or'] if keyword in direc), None)
                    if keyword_found:
                        keyword_found = "or from AsiaWorld-Expo" if keyword_found == "to or" else keyword_found
                        converted += f"Airport line to {keyword_found}: "
                    else:
                        train_line, laststation = direc.split(' to ')
                        if train_line in LINE_CONVERSION.keys():
                            train_line = LINE_CONVERSION[train_line]
                        if laststation in STATION_CONVERSION.keys():
                            laststation = STATION_CONVERSION[laststation]
                        converted += f"{train_line} to {laststation}: "
                coordinate_sets = coordinates.split(' ; ')
                for coordinate_set in coordinate_sets:
                    sumX = 0
                    sumY = 0
                    count = 0
                    for coordinate in coordinate_set.split('),('):
                        x, y = map(int, coordinate.strip('()').split(','))
                        sumX += x
                        sumY += y
                        count += 1
                    avgX = sumX / count
                    avgY = sumY / count
                    converted += f"{avgX},{avgY} ; "
                converted = converted[:-3] + '\n'

            final_output = {}
            for file_line in converted.split('\n'):
                if not file_line.strip():
                    continue
                key, coords = file_line.split(': ')
                coords = coords.split(' ; ')
                for coord in coords:
                    if key in final_output:
                        final_output[key] += [coord.split(',')[0], coord.split(',')[1]]
                    else:
                        final_output[key] = [coord.split(',')[0], coord.split(',')[1]]


            with open('station_data_json/'+file.replace('.txt', '.json'), 'w', encoding='utf-8') as f2:
                json.dump(final_output, f2, ensure_ascii=False, indent=4)
            
    # remove all txt files
    for file in os.listdir('stationdata'):
        os.remove('stationdata/'+file)
    # remove directory
    os.rmdir('stationdata')
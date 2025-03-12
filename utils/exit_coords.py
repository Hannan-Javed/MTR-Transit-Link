import os, re, json

def convert_to_old(exits, old_dpi=250, new_dpi=1000):
    for key in exits:
        exits[key] = [coord * old_dpi / new_dpi for coord in exits[key]]
    return exits

def valid_exit(exit):
    return not not re.match(r'^[A-HJ-LNPR]\d?$', exit)

def clean_exits_data(exits):

    grouped_exits = {}
    for exit in exits.keys():
        if exit[0].isalpha() and len(exit) >= 2:
            if exit[0] not in grouped_exits:
                grouped_exits[exit[0]] = []
            grouped_exits[exit[0]].append(exit[1] if len(exit) == 2 else '9')

    # fill any missing digit
    # e.g. change {'B2': [...], 'B': [...], B123: [...], BQ: [...]} to {'B2': [...], 'B': [...], B1: [...], , B3: [...]}
    for key, digits in grouped_exits.items():
        # special case - if there was only B1, then another must be B2
        # e.g. for changing {'B1': [...], 'B': [...], BQ: [...]} to {'B2': [...], 'B': [...], B1: [...]}
        digits.sort()
        if len(digits) == 2:
            if digits[0] == '1' and digits[1] != '2':
                same_other_exit = next((exit for exit in exits.keys() if key == exit[0] and len(exit) >= 2 and exit [1:]!= '1'), None)
                if same_other_exit is not None:
                    new_exit = key + '2'
                    exits[new_exit] = exits.pop(same_other_exit)
                break
 
        for i in range(1, len(digits) + 1):
            if str(i) not in digits:
                old_exit = next((
                                exit for exit in sorted(
                                    exits.keys(),
                                    key=lambda ex: int(ex[1:]) if ex[1:].isdigit() else -1,
                                    reverse=True
                                )
                                if len(exit) >= 2 and key == exit[0]
                                ),  None)
                if old_exit is None:
                    continue
                new_exit = key + str(i)
                exits[new_exit] = exits.pop(old_exit)
    
    # if some exit still does not follow format, then look for missing digits
    # e.g. change {'A': [...], 'B': [...], 'D': [...], '123': [...]} to {'A': [...], 'B': [...], 'D': [...], 'C': [...]}
    if not all([valid_exit(exit) for exit in exits.keys()]):
        distinct_alphabets = set([exit[0] for exit in exits.keys() if exit[0].isalpha()])
        if len(distinct_alphabets) == 0:
            all_alphabets = set(chr(i) for i in range(ord('A'), ord('A') + len(exits))) - {'I', 'M', 'O', 'Q'}
        else:
            all_alphabets = set(chr(i) for i in range(ord('A'), ord(max(distinct_alphabets)) + 1)) - {'I', 'M', 'O', 'Q'}
        missing_alphabets = sorted(all_alphabets - distinct_alphabets)
        if missing_alphabets:
            for alphabet in missing_alphabets:
                for exit in list(exits.keys()):
                    if not exit[0].isalpha() or not valid_exit(exit):
                        exits[alphabet] = exits.pop(exit)
                        break
                
    def sort_exit_key(key):
        if len(key) == 1:
            return (key, 0)
        return (key[0], int(key[1:]) if key[1:].isdigit() else 0)

    exits = dict(sorted(exits.items(), key=lambda item: sort_exit_key(item[0])))
    return exits

def save_exits_data(stations_exits):
    
    os.makedirs('exits_data_json', exist_ok=True)
    for station, exits in stations_exits.items():
        new_exits = clean_exits_data(exits)
        new_exits = convert_to_old(new_exits, old_dpi = 250, new_dpi = 1000)
        with open('exits_data_json/'+station+'.json', 'w', encoding='utf-8') as f:
            json.dump(new_exits, f, ensure_ascii=False, indent=4)
        
        if exits != new_exits:
            with open('exits.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Coordinates of station {station} have been modified.\n")

        # might be the case of still some out-of-format keys. In that case, have to do manually
        if not all([valid_exit(exit) for exit in new_exits.keys()]):
            with open('exits.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Station {station} has invalid exits format.\n")
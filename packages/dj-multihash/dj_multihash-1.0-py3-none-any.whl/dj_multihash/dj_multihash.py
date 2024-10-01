import hashlib
import json
import os

def hashstring256(layers:int,string:str):
    file = json.load(open(os.path.expanduser("~/multihash.json"),"r"))
    value = ""
    for _ in range(layers):

        salt_string = None
        for item in file:
            if isinstance(item, dict) and "salt_string" in item:
                salt_string = item["salt_string"]
                break

        finalstring = string + salt_string
        hashed_string = hashlib.sha256(finalstring.encode()).hexdigest()
        # list_final_chars = list(hashed_string)
        if value == "":
            final_string_to_return = list(hashed_string)
        else:
            final_string_to_return = list(value + salt_string)

        final_string_to_return_last = ""
        for item in file:
            for char in final_string_to_return:
                if char in item:
                    final_string_to_return_last = f"{final_string_to_return_last}{item[char]}"

        value = final_string_to_return_last
    
    return value


import re
from datetime import datetime
from django.conf import settings


def enter_directory(dir_name):
    input_string = dir_name

    # Find the index of "cd" in the input string
    cd_index = input_string.find("cd")

    if cd_index != -1:
        # Extract the text after "cd"
        extracted_text = input_string[cd_index + 3 :]

        # Check if there's a forward slash in the extracted text
        if "/" in extracted_text:
            slash_index = extracted_text.find("/")

            if slash_index != -1:
                # Extract the text before the first "/"
                extracted_folder = extracted_text[:slash_index]
                print("Folder name:", extracted_folder)
        else:
            return extracted_text
        return extracted_text
    else:
        return "No match found."

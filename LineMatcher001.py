"""
Script to read lines from a log file, check if each line is a substring of the next line, 
and categorize them into 'found' and 'not found' lists.

Sample Input:
    File "input_file_name.log | txt" contains:
        [
            "Error: Connection lost",
            "Error: Connection lost. Retrying...",
            "User logged in",
            "User logged in successfully",
            "Unexpected end of input",
            "",
            "Another log entry",
            "No matching substring"
        ]

Expected Output:
    Found lines:
    Error: Connection lost
    User logged in
    --------------------------------
    Not found lines:
    Unexpected end of input
    Another log entry
    No matching substring
    --------------------------------
    Result dictionary:
    {'Error: Connection lost': 'Found'}
    {'User logged in': 'Found'}
    {'Unexpected end of input': ''}
    {'Another log entry': ''}
    {'No matching substring': ''}

Functions:
    - read_file_to_lines(file_name, folder_path): Reads the content of a file and returns it as a list of lines.
    - remove_empty_lines(lines): Removes any empty lines from a list of lines.
"""

import os

def main():
    # Read lines from the specified log file
    reading_lines = read_file_to_lines("input_file_name.log") # change the file name and 
            ## add the path to file as second argument if the file is not in same location of the file script

    # Remove any empty lines from the list of lines
    filtered_lines = remove_empty_lines(reading_lines)

    # Initialize lists to store found and not found lines, and a result dictionary to store the results
    found_list = []
    not_found_list = []
    result_dict = []
    i = 0

    # Iterate through the filtered lines
    while i < len(filtered_lines)-1:
        # Check if the current line is a substring of the next line
        if filtered_lines[i].strip() in filtered_lines[i+1]:
            # If found, add the current line to the found_list and result_dict with 'Found' status
            found_list.append(filtered_lines[i].strip())
            result_dict.append({filtered_lines[i].strip(): 'Found'})
            # Skip to the next pair of lines
            i = i + 2
        else:
            # If not found, add the current line to the not_found_list and result_dict with an empty status
            not_found_list.append(filtered_lines[i].strip())
            result_dict.append({filtered_lines[i].strip(): ''})
            # Move to the next line
            i = i + 1
    
    # Print all lines that were found
    print("Found String")
    [print(line) for line in found_list]
    print('---------- End of Found String ----------------')

    # Print all lines that were not found
    print("Not Found String")
    [print(line) for line in not_found_list]
    print('---------- End of Not Found String ----------------')

    # Print the result dictionary containing all lines and their status
    print("String As Dict")
    [print(line) for line in result_dict]
        
def read_file_to_lines(file_name, folder_path = ''):
    """ Read file and return it in list of lines """
    file_path = os.path.join(folder_path, file_name) if folder_path else file_name
    file_obj = open(file_path, "r")
    lines = file_obj.readlines()
    file_obj.close()
    return lines

def remove_empty_lines(lines):
    """Remove empty lines from a list of lines."""
    return [line for line in lines if line.strip() ]


main()


import os
import json
import argparse
from typing import List, Any

def load_project_config(config_path: str, project_name: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    projects = data.get("projects", {})
    if project_name not in projects:
        available = ", ".join(projects.keys())
        raise ValueError(f"Unknown project '{project_name}'. Available: {available}")

    cfg = projects[project_name]

    # small defaults so config can be minimal
    cfg.setdefault("exclude_dirs_list", [])
    cfg.setdefault("exclude_files_list", [])
    cfg.setdefault("include_files_extensions", [])
    cfg.setdefault("output_file_name", "export_output")
    cfg.setdefault("output_file_path", "")

    return cfg

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="export_config.json")
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    cfg = load_project_config(args.config, args.project)

    fetch_path = cfg["fetch_path"]
    root_dir_name = cfg["root_dir_name"]
    exclude_dirs_list = cfg["exclude_dirs_list"]
    exclude_files_list = cfg["exclude_files_list"]
    include_files_extensions = cfg["include_files_extensions"]
    output_file_name = cfg["output_file_name"]
    output_file_path = cfg["output_file_path"]
    output_version = cfg["version"]

    # read files from folder
    files = list_files_with_extensions(fetch_path, exclude_dirs_list, exclude_files_list, include_files_extensions )
    # [print(file) for file in files]
    # exit()
    chunk_files = split_list_into_chunks(files, 7)
    for ind, files in enumerate(chunk_files):
        # current_output_file = output_file_name + f"_{ind}.log"
        current_output_file = f"{output_file_name}_{output_version}_file.log"
        for file in files:
            folder = get_folder_path_from_root(file, root_dir_name)
            file_name = os.path.basename(file)
            print(f"Processing: {os.path.join(folder, file_name)}")
            lines = read_file_to_lines(file)
            # lines = remove_empty_lines(lines)
            write_to_file_from_str("\n========================================================", current_output_file, output_file_path)
            write_to_file_from_str(os.path.join(folder, file_name), current_output_file, output_file_path)
            write_to_file_from_str("-------------------------", current_output_file, output_file_path)
            write_to_file_from_list(lines, current_output_file, output_file_path)

    print("Please check output file")

def list_files_with_extensions(folder_path, exclude_dirs_list=[], exclude_files_list=[], include_files_extensions=[]):
    """
    Lists files from a directory and its subdirectories, including only the specified file extensions.
    
    :param folder_path: The root directory to search for files.
    :param exclude_dirs_list: A list of directory names to exclude from the search.
    :param exclude_files_list: A list of specific file names to exclude from the search.
    :param include_files_extensions: A list of file extensions to include (e.g., ['.ts', '.tsx']).
    :return: A list of filtered files with full paths.
    """
    filtered_files = []
    
    for path, subdirs, files in os.walk(folder_path):
        # Exclude directories specified in exclude_dirs_list
        subdirs[:] = [d for d in subdirs if d not in exclude_dirs_list]  # Modify subdirs in place

        # Filter files based on the include_files_extensions and exclude_files_list
        for file in files:
            file_path = os.path.join(path, file)

            # Skip if the file is in the exclude_files_list
            if file in exclude_files_list:
                continue

            # Include files with the specified extensions only
            if include_files_extensions and any(file.endswith(ext) for ext in include_files_extensions):
                filtered_files.append(file_path)
    
    return filtered_files

def split_list_into_chunks(input_list: List[Any], chunk_size: int = 4) -> List[List[Any]]:
    """
    Splits a list into smaller chunks of a specified size.
    
    :param input_list: The list to be split into chunks.
    :param chunk_size: The size of each chunk. Defaults to 4.
    :return: A list of lists, where each inner list is a chunk of the original list.
    
    Example:
    --------
    split_list_into_chunks([1, 2, 3, 4, 5, 6, 7], chunk_size=3)
    -> [[1, 2, 3], [4, 5, 6], [7]]
    """
    # Validate that input_list is indeed a list
    if not isinstance(input_list, list):
        raise ValueError("input_list must be a list.")
    
    # Validate that chunk_size is a positive integer
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    # Using list comprehension to break the input_list into chunks of size chunk_size
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def get_folder_path_from_root(file_path, root_dir_name = "src"):
    """
    Get the folder path after the [root_dir_name] directory from the complete file path.
    
    :param file_path: Full file path as input.
    :return: The path after the [root_dir_name] directory, or an empty string if [root_dir_name] is not found.
    """
    path_after_src = ''  # Variable to accumulate the path after [root_dir_name]
    max_iterations = 10  # Safety limit to prevent infinite loop if [root_dir_name] is not found

    while max_iterations > 0:
        # Get the parent directory of the current file path
        parent_dir = os.path.dirname(file_path)
        
        # Get the base name of the parent directory (last part of the path)
        parent_folder_name = os.path.basename(parent_dir)
        
        # If we encounter the [root_dir_name] folder, break out of the loop
        if parent_folder_name == root_dir_name:
            break
        
        # Accumulate the path after [root_dir_name] in reverse order
        path_after_src = os.path.join(parent_folder_name, path_after_src)

        # Move up one directory level
        file_path = parent_dir
        
        max_iterations -= 1  # Decrement safety counter

    # If [root_dir_name] was not found after 10 iterations, return an empty string
    if max_iterations == 0:
        print(f"Warning: {root_dir_name} folder not found in the given path.")
        return ''
    
    return os.path.join(root_dir_name, path_after_src)

def read_file_to_lines(file_name, folder_path=None):
    """
    Read the contents of a file and return it as a list of lines.
    
    :param file_name: The name of the file to read.
    :param folder_path: Optional folder path where the file is located. Defaults to current directory.
    :return: A list of lines from the file.
    """
    # Determine the full file path; if no folder path is provided, use the file name only
    file_path = os.path.join(folder_path, file_name) if folder_path else file_name
    
    try:
        # Using 'with' ensures the file is properly closed after reading
        with open(file_path, "r", errors='ignore') as file_obj:
            lines = file_obj.readlines()  # Read all lines from the file into a list
        return lines
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found at '{file_path}'")
        return []
    except IOError as e:
        print(f"Error reading file '{file_name}': {e}")
        return []

def write_to_file_from_str(var_str, file_name, file_path=None):
    """
    Write a string to a file.
    
    :param var_str: The string to be written to the file.
    :param file_name: The name of the file where the string should be saved.
    :return: None
    """

    # Build the full file path
    save_path = os.path.join(file_path, file_name) if file_path else file_name

    try:
        # Use 'with' to safely open and close the file
        with open(save_path, "a") as file_obj:
            file_obj.write(var_str)  # Write the string to the file
            file_obj.write("\n")
        print(f"Successfully written to file: {save_path}")
    
    except IOError as e:
        # Handle I/O errors, such as file permission issues or invalid paths
        print(f"Error writing to file '{file_name}': {e}")

def write_to_file_from_list(lst, file_name, file_path=None):
    """
    Writes a list of strings to a file.
    
    :param lst: List of strings to be written to the file.
    :param file_name: The name of the file where the content should be written.
    :param file_path: Optional file path where the file should be saved. Defaults to the current directory.
    :return: None
    """
    # Ensure the full file path is constructed properly, even if no folder is provided
    full_path = os.path.join(file_path, file_name) if file_path else file_name

    # Ensure that 'lst' is a list of strings
    if not isinstance(lst, list):
        print("Error: Input is not a list. No content will be written.")
        return

    try:
        # Open the file for writing using 'with' to ensure proper file handling
        with open(full_path, "a") as file_obj:
            # Write each item from the list to the file
            for line in lst:
                if not isinstance(line, str):
                    print(f"Warning: Non-string item '{line}' found in list. Skipping.")
                    continue
                file_obj.write(line)
        print(f"Successfully written to file: {full_path}")
    
    except IOError as e:
        # Handle potential I/O errors during file writing
        print(f"Error writing to file '{full_path}': {e}")


def list_files_excluding_extensions(folder_path, exclude_dirs_list=[], exclude_files_list=[], exclude_files_extensions=[]):
    """
    Lists files from a directory and its subdirectories, excluding specified file extensions.
    
    :param folder_path: The root directory to search for files.
    :param exclude_dirs_list: A list of directory names to exclude from the search.
    :param exclude_files_list: A list of specific file names to exclude from the search.
    :param exclude_files_extensions: A list of file extensions to exclude (e.g., ['.ts', '.tsx']).
    :return: A list of filtered files with full paths.
    """
    filtered_files = []
    
    for path, subdirs, files in os.walk(folder_path):
        # Exclude directories specified in exclude_dirs_list
        subdirs[:] = [d for d in subdirs if d not in exclude_dirs_list]  # Modify subdirs in place

        # Filter files based on the exclude_files_extensions and exclude_files_list
        for file in files:
            file_path = os.path.join(path, file)

            # Skip if the file is in the exclude_files_list
            if file in exclude_files_list:
                continue

            # Skip files with the specified extensions to exclude
            if exclude_files_extensions and any(file.endswith(ext) for ext in exclude_files_extensions):
                continue

            filtered_files.append(file_path)
    
    return filtered_files

def get_parent_folder_name(file_path):
    """
    Get the parent folder name from the complete file path.
    
    :param file_path: Full file path.
    :return: Name of the parent folder.
    """
    parent_dir = os.path.dirname(file_path)  # Get the parent directory
    parent_folder_name = os.path.basename(parent_dir)  # Get the last part (folder name)
    return parent_folder_name

def remove_empty_lines(lines):
    """
    Remove empty lines from a list of lines.
    
    :param lines: A list of lines (strings), possibly containing empty lines or lines with only whitespace.
    :return: A new list with all empty lines removed. A line is considered 'empty' if it contains only whitespace characters.
    """
    # Ensure the input is a list, return an empty list if it's not
    if not isinstance(lines, list):
        print("Warning: Input is not a list. Returning an empty list.")
        return []

    # List comprehension that filters out lines that are empty or contain only whitespace
    return [line for line in lines if line.strip()]


main()
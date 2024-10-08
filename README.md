# Extract Files To Text Script Documentation

## Overview

This script processes files in a directory by filtering them based on specified extensions and exclusions. It reads the content of the filtered files, splits them into chunks, and writes each chunk to an output file. The script is designed to operate recursively through subdirectories and can exclude certain directories and files from its operations.

## Functions

### `main()`

- The entry point of the script. It defines several configurations like the directory to search, the files and directories to exclude, and the file extensions to include.
- It then calls helper functions to list files, chunk them, read their content, and write the content into log files.
- Output files are saved as separate logs with incremental numbering (`_0.log`, `_1.log`, etc.).

### `list_files_with_extensions(folder_path, exclude_dirs_list, exclude_files_list, include_files_extensions)`

Lists files from a directory and its subdirectories, including only files with specified extensions and excluding specific directories or files.

- **Parameters**:
  - `folder_path`: Path of the directory to search.
  - `exclude_dirs_list`: List of directories to exclude from the search.
  - `exclude_files_list`: List of specific files to exclude.
  - `include_files_extensions`: List of file extensions to include (e.g., `['.ts', '.tsx']`).
- **Returns**: A list of full file paths that match the criteria.

### `list_files_excluding_extensions(folder_path, exclude_dirs_list, exclude_files_list, exclude_files_extensions)`

Similar to `list_files_with_extensions()`, but instead excludes files with certain extensions.
**The main difference** here is if you use this function with default empty `exclude_files_extensions` (e.g., `[]`) the function **will return all the files under folder path except the excluded dirs and files**.

- **Parameters**:
  - Similar to `list_files_with_extensions`, but filters based on extensions to exclude.
- **Returns**: A list of files that don’t match the excluded extensions.

### `get_parent_folder_name(file_path)`

Extracts and returns the name of the parent folder from a given file path.

- **Parameters**:
  - `file_path`: Full path of the file.
- **Returns**: The parent folder name as a string.
  **Example**:

```python
file_path = r"D:\Programming\parent_project\src\file.ts"
parent_folder = get_parent_folder_name(file_path)
print(parent_folder)  # Output: "src"
```

### `get_folder_path_from_root(file_path, root_dir_name="src")`

Traverses the directory structure starting from the root folder (`root_dir_name`) and returns the path of a file relative to this folder.

- **Parameters**:
  - `file_path`: Full path of the file.
  - `root_dir_name`: Name of the root directory to find.
- **Returns**: The relative path after the root folder or an empty string if the root is not found.

```python
file_path = r"D:\Programming\parent_project\src\components\header\header.tsx"
folder_path = get_folder_path_from_root(file_path, root_dir_name="src")
print(folder_path)  # Output: "src\components\header"
```

### `read_file_to_lines(file_name, folder_path=None)`

Reads the content of a file and returns it as a list of lines.

- **Parameters**:
  - `file_name`: Name of the file to read.
  - `folder_path`: Optional path to the folder containing the file. Defaults to current directory.
- **Returns**: A list of strings representing lines in the file. Returns an empty list if the file is not found.

### `remove_empty_lines(lines)`

Removes empty lines from a list of strings.

- **Parameters**:
  - `lines`: A list of strings, possibly containing empty lines.
- **Returns**: A new list with empty lines removed.

### `write_to_file_from_str(var_str, file_name, file_path=None)`

Writes a string to a file. Appends to the file if it already exists.

- **Parameters**:
  - `var_str`: The string to write to the file.
  - `file_name`: The name of the file to write to.
  - `file_path`: Optional path where the file is saved. Defaults to current directory.

### `write_to_file_from_list(lst, file_name, file_path=None)`

Writes a list of strings to a file, each string on a new line. Appends to the file if it already exists.

- **Parameters**:
  - `lst`: List of strings to write to the file.
  - `file_name`: Name of the file to write to.
  - `file_path`: Optional folder path to save the file in. Defaults to current directory.

### `split_list_into_chunks(input_list: List[Any], chunk_size: int = 4)`

Splits a list into smaller chunks of a specified size.

- **Parameters**:
  - `input_list`: The list to be split.
  - `chunk_size`: The size of each chunk. Defaults to 4.
- **Returns**: A list of lists, where each sublist is a chunk of the original list.

  **Example**:

  ```python
  split_list_into_chunks([1, 2, 3, 4, 5, 6, 7], chunk_size=3)
  # -> [[1, 2, 3], [4, 5, 6], [7]]
  ```

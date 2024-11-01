# Extract Files To Text Script Documentation [extract_files_to_text.py]

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

# File Encryption and Decryption Script [encrypt_file_content.py]

## Overview

This script provides encryption and decryption functionality for file content, specifically targeting unique words, IP addresses, and ports. During encryption, each word, IP, and port is replaced with a randomly generated substitute that is unique and consistent throughout the file. This allows identical values in the original content to be replaced with the same substitute value. The encryption mappings are saved to a CSV file, enabling decryption to restore the original content.

### Key Features

1. **Encryption**:
   - Replaces words, IP addresses, and ports with unique, randomized substitutes.
   - Stores mappings in a CSV file to ensure consistent replacements across the file.
2. **Decryption**:
   - Uses stored mappings to restore encrypted content to its original form.

### Usage

Run the script from the command line with one of two modes, `encrypt` or `decrypt`, along with the input file path and the output file path.

#### Encrypting a File

To encrypt a file:

```bash
python script.py -e input.txt encrypted_output.txt
# or
python script.py --encrypt input.txt encrypted_output.txt

```

- `input.txt`: Path to the file to be encrypted.
- `encrypted_output.txt`: Path where encrypted content will be saved.
- A `mappings.csv` file will be generated in the same directory as `input.txt` to store the mappings for decryption.

#### Decrypting a File

To decrypt a file:

```bash
python script.py -e input.txt encrypted_output.txt
# or
python script.py --encrypt input.txt encrypted_output.txt

```

- `encrypted_output.txt`: Path to the file to be decrypted.
- `decrypted_output.txt`: Path where decrypted content will be saved.
- The `mappings.csv` file generated during encryption must be in the same directory as `encrypted_output.txt`.

## Functions

### main()

- **Purpose**: Parses command-line arguments.
- **Details**:
  - Accepts `-e` or `--encrypt` for encryption and `-d` or `--decrypt` for decryption.
  - Identifies the input and output file paths.
  - Determines the mode and calls the respective `encrypt_content` or `decrypt_content` function.

### encrypt_content(input_file, output_file, mappings_file_path)

- **Purpose**: Encrypts file content by replacing each word, IP, and port with a unique substitute.
- **Parameters**:
  - `input_file`: Path to the file to be encrypted.
  - `output_file`: Path where the encrypted content will be saved.
  - `mappings_file_path`: Path to the CSV file storing mappings for decryption.
- **Process**:
  - Scans the file to identify and replace words, IPs, and ports.
  - Writes the encrypted content to `output_file`.
  - Saves original-to-substitute mappings in `mappings.csv`.

### decrypt_content(encrypted_file_path, mappings_file_path, decrypted_file)

- **Purpose**: Decrypts the encrypted content by restoring the original values using mappings stored in `mappings.csv`.
- **Parameters**:
  - `encrypted_file_path`: Path to the encrypted file to be decrypted.
  - `mappings_file_path`: Path to the CSV file storing mappings used for decryption.
  - `decrypted_file`: Path where the decrypted content will be saved.
- **Process**:
  - Loads mappings from `mappings.csv`.
  - Reverses replacements in `encrypted_file_path` to restore original values.
  - Writes decrypted content to `decrypted_file`.

### generate_word_replacement(word)

- **Purpose**: Generates a unique replacement word in the format `word_XXXX`.
- **Details**: Ensures each generated word is unique within the encryption session.

### generate_ip_replacement()

- **Purpose**: Generates a unique IP address for replacement.
- **Details**: Ensures no duplicate or original IP is used as a replacement.

### generate_port_replacement()

- **Purpose**: Generates a unique port for replacement.
- **Details**: Ensures no duplicate or original port is used as a replacement.

### extract_existing_ips(file_path)

- **Purpose**: Extracts all IPs from the input file to avoid duplicates in replacements.

### extract_existing_ports(file_path)

- **Purpose**: Extracts all ports from the input file to avoid duplicates in replacements.

### save_mappings_to_csv(mappings_file_path)

- **Purpose**: Saves mappings of original values to replacements in a CSV file for future decryption.

### load_mappings_from_csv(mappings_file_path)

- **Purpose**: Loads mappings from `mappings.csv` to use for decryption.

## Examples

### Encryption Example

Suppose you have a file named `sample.txt` with the following content:

```yaml
Server IP: 192.168.1.1
Server Port: 8080
Username: admin
```

To encrypt `sample.txt`, run:

```bash
python script.py -e sample.txt encrypted_sample.txt

```

After encryption, `encrypted_sample.txt` might look like this:

```yaml
Server IP: 54.235.67.89
Server Port: 2345
Username: word_5832
```

### Decryption Example

Using the above encrypted file `encrypted_sample.txt`, you can restore the original content by running:

```bash
python script.py -d encrypted_sample.txt decrypted_sample.txt

```

The decrypted content in `decrypted_sample.txt` will match the original `sample.txt` content:

```yaml
Server IP: 192.168.1.1
Server Port: 8080
Username: admin
```

## Important Notes

- **Mapping File**: The `mappings.csv` file is essential for decryption, so it should be kept safe. Without it, encrypted files cannot be decrypted back to their original content.
- **Consistency**: Identical words, IPs, and ports will always be replaced with the same generated substitutes within a single encryption session.
- **Requirements**: The script uses only Python standard libraries (`re`, `csv`, `random`, `argparse`, `os`).

## License

This project is open-source and available under the MIT License.

"""
This script provides encryption and decryption functionality for file content, specifically replacing 
each unique word, IP address, and port with randomly generated substitutes. The encrypted substitutions 
are consistent throughout the file, ensuring that identical original values are replaced with identical 
substitute values each time they appear. The script supports switching between encryption and decryption 
modes through command-line arguments.

Functionality:
1. **Encryption**:
   - Replaces words, IP addresses, and ports with randomized, unique substitutes.
   - Stores original-to-substitute mappings in a CSV file for consistent replacement across the file.
   
2. **Decryption**:
   - Uses the stored mappings in the CSV file to revert encrypted content back to its original form.

The script uses regular expressions to identify words, IPs, and ports in the file content, and stores 
the encrypted mappings in the same directory as the input file. It requires three arguments: 
either `-e`/`--encrypt` for encryption or `-d`/`--decrypt` for decryption, the input file path, and the output file path.

Usage:
Encrypting a file:
    python script.py -e input.txt encrypted_output.txt
    python script.py --encrypt input.txt encrypted_output.txt

Decrypting a file:
    python script.py -d encrypted_output.txt decrypted_output.txt
    python script.py --decrypt encrypted_output.txt decrypted_output.txt
"""

import re
import csv
import random
import argparse
import os


# Define regex patterns for words, IP addresses, and ports
WORD_PATTERN = r'\b[A-Za-z]+\b'
IP_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
PORT_PATTERN = r':\b\d{1,5}\b'  # Ports range between 1 and 65535, prefixed with a colon

# Sets to keep track of used and existing ports and IPs and used words
used_words = set()
used_ips = set()
existing_ips = set()
used_ports = set()
existing_ports = set()

# Dictionaries to store mappings of original to replacement values for words, IPs, and ports
word_mapping = {}
ip_mapping = {}
port_mapping = {}

def main():
    """
    Main function that parses command-line arguments for input and output file paths and
    initiates the encryption or decryption process. Usage example:
        python script.py -e input.txt encrypted_output.txt
        python script.py -d encrypted_output.txt decrypted_output.txt
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt content in a file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the input file.")
    group.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the input file.")
    parser.add_argument("input_file", help="Path to the input file to encrypt.")
    parser.add_argument("output_file", help="Path to the output file for encrypted content.")
    
    args = parser.parse_args()

    # Extract the directory of the input file and set mapping file path
    input_dir = os.path.dirname(args.input_file)
    mapping_file = os.path.join(input_dir, 'mappings.csv')
    
    # Perform encryption or decryption based on the mode
    if args.encrypt:
        # Encrypt the content of the specified input file and save it to the specified output file
        encrypt_content(args.input_file, args.output_file, mapping_file)
    elif args.decrypt:
        decrypt_content(args.input_file, mapping_file, args.output_file)

def generate_word_replacement(word):
    """Generates a unique replacement word in the format 'word_XXXX', ensuring it is not already used."""
    while True:
        # Generate a random word
        word = f"word_{random.randint(1000, 9999)}"
        # Ensure it's unique and not in the existing ports
        if word not in used_words:
            used_words.add(word)
            return word

def generate_ip_replacement():
    """Generates a unique IP address for replacement, ensuring it is not already used or in the original file."""
    while True:
        # Generate a random port within the valid range
        ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        # Ensure it's unique and not in the existing ports
        if ip not in used_ips and ip not in existing_ips:
            used_ips.add(ip)
            return ip

def generate_port_replacement():
    """Generates a unique port for replacement, ensuring it is not already used or in the original file."""
    while True:
        # Generate a random port within the valid range
        port = str(random.randint(1024, 65535))
        # Ensure it's unique and not in the existing ports
        if port not in used_ports and port not in existing_ports:
            used_ports.add(port)
            return port

def extract_existing_ips(file_path):
    """Extracts all IPs from the input file and stores them in existing_ips to avoid duplicates in replacements."""
    with open(file_path, 'r') as f:
        content = f.read()
        matches = re.findall(IP_PATTERN, content)
        for match in matches:
            existing_ips.add(match)

def extract_existing_ports(file_path):
    """Extracts all ports from the input file and stores them in existing_ports to avoid duplicates in replacements."""
    with open(file_path, 'r') as f:
        content = f.read()
        matches = re.findall(PORT_PATTERN, content)
        # Strip the leading colon and add to the existing_ports set
        for match in matches:
            port = match[1:]  # Remove the leading colon
            existing_ports.add(port)

def encrypt_content(file_path, output_file, mappings_file_path):
    """
    Encrypts the content of the input file by replacing each word, IP, and port with a unique substitute.
    Saves the encrypted content to the output file.
    """

    # Extract existing IPs and ports from the file to avoid collisions in replacements
    extract_existing_ports(file_path)
    extract_existing_ips(file_path)

    with open(file_path, 'r') as f:
        content = f.read()
        
        # Replace each unique word with a generated replacement word
        content = re.sub(WORD_PATTERN, lambda match: word_mapping.setdefault(
            match.group(0), generate_word_replacement(match.group(0))
        ), content)
        
        # Replace each unique IP with a generated replacement IP
        content = re.sub(IP_PATTERN, lambda match: ip_mapping.setdefault(
            match.group(0), generate_ip_replacement()
        ), content)
        
        # Replace each unique port with a generated replacement port
        content = re.sub(PORT_PATTERN, lambda match: port_mapping.setdefault(
            match.group(0), ":" + generate_port_replacement()
        ), content)
    
    # Save mappings to a CSV file to preserve the replacement data for decryption
    save_mappings_to_csv(mappings_file_path)
    
    # Write the encrypted content to the specified output file
    with open(output_file, 'w') as f:
        f.write(content)

def save_mappings_to_csv(mappings_file_path):
    """Saves the mappings of original values to replacements in a CSV file for future decryption."""
    with open(mappings_file_path, 'w', newline='') as csvfile:
        fieldnames = ['original', 'replacement', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Write word mappings
        for original, replacement in word_mapping.items():
            writer.writerow({'original': original, 'replacement': replacement, 'type': 'word'})
        
        # Write IP mappings
        for original, replacement in ip_mapping.items():
            writer.writerow({'original': original, 'replacement': replacement, 'type': 'ip'})
        
        # Write port mappings
        for original, replacement in port_mapping.items():
            writer.writerow({'original': original, 'replacement': replacement, 'type': 'port'})

def decrypt_content(encrypted_file_path, mappings_file_path, decrypted_file):
    """
    Decrypts the encrypted content by reversing replacements based on mappings stored in the CSV file.
    Writes the decrypted content to a new file decrypted_file.
    """
    
    # Load the mappings from CSV to reverse the encryption process
    load_mappings_from_csv(mappings_file_path)
    
    with open(encrypted_file_path, 'r') as f:
        content = f.read()
        
        # Reverse replacements for words, IPs, and ports based on stored mappings
        for replacement, original in {v: k for k, v in word_mapping.items()}.items():
            content = content.replace(replacement, original)
        for replacement, original in {v: k for k, v in ip_mapping.items()}.items():
            content = content.replace(replacement, original)
        for replacement, original in {v: k for k, v in port_mapping.items()}.items():
            content = content.replace(replacement + " ", original + " ")
    
    # Write the decrypted content to a new file
    with open(decrypted_file, 'w') as f:
        f.write(content)

def load_mappings_from_csv(mappings_file_path):
    """Loads mappings from a CSV file to restore the original values for decryption."""

    with open(mappings_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type'] == 'word':
                word_mapping[row['original']] = row['replacement']
            elif row['type'] == 'ip':
                ip_mapping[row['original']] = row['replacement']
            elif row['type'] == 'port':
                port_mapping[row['original']] = row['replacement']

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

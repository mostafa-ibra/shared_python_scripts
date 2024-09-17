#!/usr/bin/python3
"""
"""
import os

def read_file_to_lines(file_name, folder_path = ''):
    """ Read file and return it in list of lines """
    file_path = os.path.join(folder_path, file_name) if folder_path else file_name
    file_obj = open(file_path, "r")
    lines = file_obj.readlines()
    file_obj.close()
    return lines

def remove_empty_lines(lines):
    return [line for line in lines if line.strip() ]
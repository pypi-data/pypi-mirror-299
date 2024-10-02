import re
import os
import subprocess
from pathlib import Path 
from datetime import datetime 
from collections.abc import Iterable

def format_filepath(output_file):
    slash = re.compile(r'[/\\]')
    if slash.search(output_file):
        scan_dir = '/'.join(output_file.split('/')[:-1])
        output_file = (output_file.split('/')[-1])
    else:
        scan_dir = Path(__file__).parent.parent / 'scan-results'

    base_output, ext = os.path.splitext(output_file)

    if not os.path.exists(scan_dir):
        os.makedirs(scan_dir)

    return scan_dir, base_output, ext.lstrip('.')

def unique_file(base_name, extension, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = f"{base_name}.{extension}"
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(file_path):
        return file_path
    i = 1
    while True:
        file_name = f"{base_name}-{i}.{extension}"
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            return file_path
        i += 1

def copy_to_nmap_dir(merged_output):
    nmap_dir = Path.home() / 'NMAP'
    if not os.path.exists(nmap_dir):
        os.makedirs(nmap_dir)

    default_dir_regex = re.compile(r'vinmap/scan-results')

    final_output_file = nmap_dir / merged_output.split('/')[-1]
    if os.path.exists(final_output_file):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        final_output_file = nmap_dir / f'{final_output_file.stem}_{current_time}{final_output_file.suffix}' 
    subprocess.run(['cp', merged_output, final_output_file])
    
    if default_dir_regex.search(merged_output):
        print(f"Deleting:\n{merged_output}\nLeaving:\n{final_output_file}")
        file_cleanup(merged_output)

    return final_output_file

def file_cleanup(filenames):
    if isinstance(filenames, str):
        filenames = [filenames]
    for filename in filenames:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted: {filename}")
        else:
            print(f"File not found: {filename}")


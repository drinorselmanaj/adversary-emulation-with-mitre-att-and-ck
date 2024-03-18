#!/bin/bash
# Set the encryption key and directory path
key='dappertest'
dir_path='/home/sambacry/'
# Move to the root directory
cd "$dir_path"
# List all files and their names in the directory recursively
file_list=$(find . -type f -name "*" -not -name ransomwaremessage.txt)
# Loop through each file in the directory
for file_path in $file_list do
 # Get the current file name
file_name=$(basename "$file_path")
# Decrypt the file using the encryption key
echo "Decrypting file: $file_name"
ccrypt -f -q -d "$file_path" -K "$key" done
    # Go back to original directory
cd "$OLDPWD"

# Make Encrypted Backup of Directory
# Using GPG (GNU Privacy Guard)

import os

input_dir = '/input_dir/'
output_dir = '/output_dir/'
passphrase = '/passphrase.txt'
extensions = {'.zip','.bak'}
encrypted_extension = '.gpg'

#
# make encrypted copy of files matching extensions
#

path_matches = []

# get paths of input files matching extension recusively
for root, dirs, input_files in os.walk(input_dir):
    for input_file in input_files:
        for i, extension in enumerate(extensions):
                if input_file.endswith(extension):
                     path_matches.append(os.path.join(root, input_file))

# encrypt each file found to new directory
for file_input_path in path_matches:
        file_output_path = file_input_path.replace(input_dir, output_dir, 1) + encrypted_extension
        file_output_dir = os.path.dirname(file_output_path)

        # make directory, if not exist
        if not os.path.exists(file_output_dir):
                print('Make folder ' + file_output_dir)
                os.makedirs(file_output_dir)

        # check if file output file exists
        if os.path.isfile(file_output_path):
                # check timestamp on file
                file_input_last_modified = os.stat(file_input_path).st_mtime

                # check timestamp on output file
                file_output_last_modified = os.stat(file_output_path).st_mtime

                # skip already existing item
                if (file_input_last_modified < file_output_last_modified):
                        print('Skipping existing ' + file_input_path + ' to ' + file_output_path)
                        continue

        print('Encrypting ' + file_input_path + ' to ' + file_output_path);

        # process as batch to automatically rewrite files
        command = 'gpg --cipher-algo AES256 --batch --yes --passphrase ' + passphrase + ' --output ' + file_output_path + ' --symmetric ' + file_input_path
        os.system(command)

#
# delete old files no longer in input_dir
#

output_path_matches = []

# get paths of input files matching extension recusively
for root, dirs, output_files in os.walk(output_dir):
    for output_file in output_files:
        file_output_path = os.path.join(root, input_file)
        file_input_path = file_output_path[:-len(encrypted_extension)]

        if os.path.isfile(file_input_path):
                continue

        if os.path.isfile(file_output_path):
                print('Remove missing ' + file_output_path)
                os.remove(file_output_path)

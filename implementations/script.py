# script.py
import os
import subprocess

# Directory containing the files
directory = '0102'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):  # Assuming the files are JSON
        file_path = os.path.join(directory, filename)
        
        # Construct the command to run the main script with the file path
        command = [
            'python', 'main_critic.py',  # Adjust the command if needed
            '-i', file_path,
            '-q', queue_path,
            '-n', str(n_process),
            '-r', result_dir_path,
            '--buffer_path', buffer_path
        ]
        
        # Execute the command
        subprocess.run(command)
import os
import subprocess
import argparse
import time
import datetime

def run_colmap(image_path, matcher_type):
    # Get the parent directory and current folder name
    parent_dir = os.path.abspath(os.path.join(image_path, os.pardir))
    current_folder_name = os.path.basename(os.path.normpath(image_path))
    
    # Check if the current folder is not named "input" and rename it if necessary
    if current_folder_name != "input":
        new_image_path = os.path.join(parent_dir, "input")
        os.rename(image_path, new_image_path)
        image_path = new_image_path
        print(f"Renamed image folder to: {image_path}")
    else:
        image_path = os.path.join(parent_dir, "input")
    
    # Define the paths for the distorted folder, database, and sparse folder
    distorted_folder = os.path.join(parent_dir, 'distorted')
    database_path = os.path.join(distorted_folder, 'database.db')
    sparse_folder = os.path.join(distorted_folder, 'sparse')

    # Create the 'distorted' and 'sparse' folders if they don't exist
    os.makedirs(distorted_folder, exist_ok=True)
    os.makedirs(sparse_folder, exist_ok=True)

    # Define the log file path
    log_file_path = os.path.join(parent_dir, "colmap_run.log")

    # Start the timer for the total time
    total_start_time = time.time()

    # Define the commands
    commands = [
        f"colmap feature_extractor --image_path {image_path} --database_path {database_path}",
        f"colmap {matcher_type} --database_path {database_path}",
        f"glomap mapper --database_path {database_path} --image_path {image_path} --output_path {sparse_folder}"
    ]

    # Run each command sequentially and log the output
    with open(log_file_path, "w") as log_file:
        log_file.write(f"COLMAP run started at: {datetime.datetime.now()}\n")
        for command in commands:
            command_start_time = time.time()
            log_file.write(f"Running command: {command}\n")
            subprocess.run(command, shell=True, check=True)
            command_end_time = time.time()
            command_elapsed_time = command_end_time - command_start_time
            log_file.write(f"Time taken for command: {command_elapsed_time:.2f} seconds\n")
            print(f"Time taken for command: {command_elapsed_time:.2f} seconds")

        # End the timer for the total time
        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time
        log_file.write(f"COLMAP run finished at: {datetime.datetime.now()}\n")
        log_file.write(f"Total time taken: {total_elapsed_time:.2f} seconds\n")
        print(f"Total time taken: {total_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run COLMAP with specified image path and matcher type.")
    parser.add_argument('--image_path', required=True, help="Path to the images folder.")
    parser.add_argument('--matcher_type', default='sequential_matcher', choices=['sequential_matcher', 'exhaustive_matcher'], 
                        help="Type of matcher to use (default: sequential_matcher).")

    # Parse the arguments
    args = parser.parse_args()

    # Run the colmap commands with the provided image_path and matcher_type
    run_colmap(args.image_path, args.matcher_type)

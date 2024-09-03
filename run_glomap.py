import os
import subprocess
import argparse
import time
import datetime
from shutil import copy2, move

def rename_image_folder_if_needed(image_path):
    # Rename the image_path folder to "source" if it's named "input" or "images"
    parent_dir = os.path.abspath(os.path.join(image_path, os.pardir))
    current_folder_name = os.path.basename(os.path.normpath(image_path))
    
    if current_folder_name in ["input", "images"]:
        new_image_path = os.path.join(parent_dir, "source")
        os.rename(image_path, new_image_path)
        print(f"Renamed image folder from {current_folder_name} to: {new_image_path}")
        return new_image_path
    return image_path

def filter_images(image_path, interval):
    parent_dir = os.path.abspath(os.path.join(image_path, os.pardir))
    input_folder = os.path.join(parent_dir, 'input')

    if interval > 1:
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)

        image_files = sorted([f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))])
        filtered_files = image_files[::interval]

        for file in filtered_files:
            copy2(os.path.join(image_path, file), os.path.join(input_folder, file))

        return input_folder
    return image_path

def run_colmap(image_path, matcher_type, interval, model_type):
    # Rename the image_path folder if needed
    image_path = rename_image_folder_if_needed(image_path)

    parent_dir = os.path.abspath(os.path.join(image_path, os.pardir))
    image_path = filter_images(image_path, interval)

    distorted_folder = os.path.join(parent_dir, 'distorted')
    database_path = os.path.join(distorted_folder, 'database.db')
    sparse_folder = os.path.join(parent_dir, 'sparse')  # Top-level sparse folder
    sparse_zero_folder = os.path.join(sparse_folder, '0')  # The new subfolder we want to create

    os.makedirs(distorted_folder, exist_ok=True)
    os.makedirs(sparse_folder, exist_ok=True)

    log_file_path = os.path.join(parent_dir, "colmap_run.log")
    total_start_time = time.time()

    # Feature extraction with enforced single camera model and PINHOLE model
    commands = [
        f"colmap feature_extractor --image_path {image_path} --database_path {database_path} --ImageReader.single_camera 1 --ImageReader.camera_model PINHOLE --SiftExtraction.use_gpu 1",
        f"colmap {matcher_type} --database_path {database_path}",
        f"glomap mapper --database_path {database_path} --image_path {image_path} --output_path {os.path.join(distorted_folder, 'sparse')} --TrackEstablishment.max_num_tracks 5000"
    ]

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

        if model_type == '3dgs':
            img_undist_cmd = (
                f"colmap image_undistorter "
                f"--image_path {image_path} "
                f"--input_path {os.path.join(distorted_folder, 'sparse/0')} "  # Use the sparse/0 in distorted
                f"--output_path {parent_dir} "  # Output undistorted results to the top-level folder
                f"--output_type COLMAP"
            )
            log_file.write(f"Running command: {img_undist_cmd}\n")
            undistort_start_time = time.time()
            exit_code = os.system(img_undist_cmd)
            undistort_end_time = time.time()
            undistort_elapsed_time = undistort_end_time - undistort_start_time

            if exit_code != 0:
                log_file.write(f"Undistortion failed with code {exit_code}. Exiting.\n")
                print(f"Undistortion failed with code {exit_code}. Exiting.")
                exit(exit_code)
            else:
                log_file.write(f"Time taken for undistortion: {undistort_elapsed_time:.2f} seconds\n")
                print(f"Time taken for undistortion: {undistort_elapsed_time:.2f} seconds")

        # Move the cameras.bin, images.bin, and points3D.bin files to sparse/0 in the top-level folder
        os.makedirs(sparse_zero_folder, exist_ok=True)
        for file_name in ['cameras.bin', 'images.bin', 'points3D.bin']:
            source_file = os.path.join(sparse_folder, file_name)
            dest_file = os.path.join(sparse_zero_folder, file_name)
            if os.path.exists(source_file):
                move(source_file, dest_file)
                log_file.write(f"Moved {file_name} to {sparse_zero_folder}\n")
                print(f"Moved {file_name} to {sparse_zero_folder}")

        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time
        log_file.write(f"COLMAP run finished at: {datetime.datetime.now()}\n")
        log_file.write(f"Total time taken: {total_elapsed_time:.2f} seconds\n")
        print(f"Total time taken: {total_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run COLMAP with specified image path and matcher type.")
    parser.add_argument('--image_path', required=True, help="Path to the images folder.")
    parser.add_argument('--matcher_type', default='sequential_matcher', choices=['sequential_matcher', 'exhaustive_matcher'], 
                        help="Type of matcher to use (default: sequential_matcher).")
    parser.add_argument('--interval', type=int, default=1, help="Interval of images to use (default: 1, meaning all images).")
    parser.add_argument('--model_type', default='3dgs', choices=['3dgs', 'nerfstudio'], 
                        help="Model type to run. '3dgs' includes undistortion, 'nerfstudio' skips undistortion.")

    args = parser.parse_args()

    run_colmap(args.image_path, args.matcher_type, args.interval, args.model_type)

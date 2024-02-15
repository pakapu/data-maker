#/bin/python3

# Generates train and val data with a percentage split

####################################
# Constants
# Be sure to change!
####################################

KEEP_UNLABELED_IMAGES = False

####################################
import shutil

from glob import glob
from os import path, mkdir
from sys import exit
from random import randrange

print("The program need a single folder with all image and label files!")
print("Note: The program will not search subfolders!\n")
data_path = input("Please enter the path to the files: ")

if not path.exists(data_path):
    print("ERROR: The path you entered does not exist!")
    exit(1)

files = glob(data_path + "/*")

files.sort()
print(f"Found {len(files)} files!")

image_save_dir = [data_path + "/train/images", data_path + "/val/images"]
label_save_dir = [data_path + "/train/labels", data_path + "/val/labels"]

if path.exists(data_path + "/train"):
    print(f"Error: Folder {data_path}/train already exists!")
    exit(1)
mkdir(data_path + "/train")
if path.exists(data_path + "/val"):
    print(f"Error: Folder {data_path}/val already exists!")
    exit(1)
mkdir(data_path + "/val")

for i in image_save_dir:
    if not path.exists(i):
        mkdir(i)
for i in label_save_dir:
    if not path.exists(i):
        mkdir(i)

files_in_val = 0
files_in_train = 0
for current_file_path in files:
    current_file_name = path.basename(current_file_path)
    current_file_name_no_ext = path.splitext(current_file_name)[0]
    #print(current_file_name, current_file_name_no_ext)

    if current_file_name[-4:] == ".txt":
    #    print("Info: Current file is a text file, skipping...")
        continue

    curr_r = randrange(0, 5) # from 0 to 4, ideally 25% of them being 0
    is_for_val = curr_r == 0
    #print(current_file_path)

    if is_for_val:
        files_in_val += 1
    #    print(" ^^^ Will be used for validation ^^^\n")
    else:
        files_in_train += 1
    #    print(" ^^^ Will be used for training ^^^\n")

    if not path.exists(data_path + '/' + current_file_name_no_ext + '.txt'):
        print(f"Info: No associated label with {current_file_name}")
        if not KEEP_UNLABELED_IMAGES:
            continue
    else:
        shutil.copy(data_path + current_file_name_no_ext + ".txt",
                    label_save_dir[is_for_val])

    shutil.copy(data_path + current_file_name,
                image_save_dir[is_for_val])


total_images = files_in_train + files_in_val
print(f"Files for training = {files_in_train}")
print(f"Files for validation = {files_in_val}")
print("Train/Val split:")
print(f"Train has {round(files_in_train / total_images * 100, 2)}%")
print(f"Val has {round(files_in_val / total_images * 100, 2)}%")

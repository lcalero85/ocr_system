import os
import glob


# method for delete use image from dirs

def delete_contents(paths):
    # input path or dirs for delete images
    extension = glob.glob(paths + '/*.jpg')
    for file in extension:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error:{e.strerror}")

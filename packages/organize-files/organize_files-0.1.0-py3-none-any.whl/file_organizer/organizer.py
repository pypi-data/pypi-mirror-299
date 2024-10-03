import os
import shutil
from pathlib import Path

music_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']
video_extensions = ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.webm']
document_extensions = ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx', '.odt']
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp']

def move_file(file_path, destination_folder):

    os.makedirs(destination_folder, exist_ok=True)

    base_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, base_name)

    if os.path.exists(destination_path):
        file_root, file_extension = os.path.splitext(base_name)
        counter = 1

        while os.path.exists(destination_path):
            new_file_name = f"{file_root}_{counter}{file_extension}"
            destination_path = os.path.join(destination_folder, new_file_name)
            counter += 1

    shutil.move(file_path, destination_path)
    print(f"Moved {file_path} to {destination_path}")


def fileOrganizer(location):
    
    for file_name in os.listdir(location):
        file_path = os.path.join(location, file_name)

        if os.path.isfile(file_path):
            file_ext = Path(file_name).suffix.lower()

            if file_ext in music_extensions:
                move_file(file_path, os.path.join(location, 'Music'))
            elif file_ext in video_extensions:
                move_file(file_path, os.path.join(location, 'Videos'))
            elif file_ext in document_extensions:
                move_file(file_path, os.path.join(location, 'Documents'))
            elif file_ext in image_extensions:
                move_file(file_path, os.path.join(location, 'Images'))
            else:
                move_file(file_path, os.path.join(location, 'Others'))

def main():
    location = input("Enter the full path of the folder : ")
    fileOrganizer(location)




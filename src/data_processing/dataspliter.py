import os
import random
import shutil
from pathlib import Path
from typing import List, Tuple

# Automate the splitting of the dataset into training, validation, and test sets



def prepare_dataset(train_ratio:float=0.7,
                    val_ratio:float=0.15, balance:bool=True) -> None:
    """
    Splits the dataset into training, validation, and test sets.
    We also label the images with the corresponding labels to be used in the YOLOv8 model.
    Hence, we create .txt files with the same name as the image files as yolo expects
    Type of yolo expected label file contents : <class_id> <x_center> <y_center> <width> <height>

    """
    # Define the paths to the dataset and the output directories
    project_root = Path(__file__).resolve().parent.parent.parent
    dataset_path = project_root / "data" / "splits"

    # Ensure the dataset path exists
    train_path = dataset_path / "train"
    val_path = dataset_path / "val"
    test_path = dataset_path / "test"

    # Create the output directories if they don't exist
    train_path.mkdir(parents=True, exist_ok=True)
    val_path.mkdir(parents=True, exist_ok=True)
    test_path.mkdir(parents=True, exist_ok=True)

    # Get a list of all image files in the raw dataset directory
    raw_dataset_path = project_root / "data" / "raw" / "thz_images"
    raw_object_path = raw_dataset_path / "object"
    raw_no_object_path = raw_dataset_path / "no_object"

    object_img = list(raw_object_path.glob("**/*.jpg"))
    no_object_img = list(raw_no_object_path.glob("**/*.jpg"))

    # count the number of images in each category
    num_object_images = len(object_img)
    num_no_object_images = len(no_object_img)
    # Combine the image lists
    # If balance is True, we will balance the dataset by taking the minimum number of images from each category
    random.seed(42)  # Set the random seed for reproducibility
    if balance:
        min_images = min(num_object_images, num_no_object_images)
        object_img = random.sample(object_img, min_images)
        no_object_img = random.sample(no_object_img, min_images)

    image_files = object_img + no_object_img

    # Shuffle the image files randomly
    random.shuffle(image_files)

    # Split the image files into training, validation, and test sets
    num_images = len(image_files)
    num_train = int(num_images * train_ratio)
    num_val = int(num_images * val_ratio)
    # num_test = num_images - (num_train - num_val)

    train_files = image_files[:num_train]
    val_files = image_files[num_train:num_train + num_val]
    test_files = image_files[num_train + num_val:]

    # copy the files to their respective directories
    # ceate the label files for each image : Type of yolo expected label file
    # contents : <class_id> <x_center> <y_center> <width> <height>

    def get_new_name(image_path:Path) -> Tuple[str, str, str]:
        """
        Get the new name for the image file.
        The new name will be the same as the original name, but with the class id and bounding box coordinates.
        """
        # Get the image name without the extension
        path = str(image_path).split(".")[0]
        image_name = path.split("/")[-1]
        sub_path = path.split("/")[-2]
        class_name = path.split("/")[-3]
        # Create the new name for the image file
        return image_name, sub_path, class_name

    def create_label_file(image_name:str, sub_path:str, class_name:str, label_path:Path) -> None:
        """
        Create a label file for the image with the same name as the image file.
        The label file will contain the class id and the bounding box coordinates.
        """
        # Create the label file path
        label_file_path = label_path / f"{class_name}_{sub_path}_{image_name}.txt"
        # Write the class id and bounding box coordinates to the label file
        with open(label_file_path, "w") as f:
            if class_name == "object":
                # If the image is an object image, we will set the class id to 0
                f.write(f"{0} 0.5 0.5 1.0 1.0")
            else:
                f.write(f"{1} 0.5 0.5 1.0 1.0")

    for file in train_files:
        # Create the label file for the image
        image_name, sub_path, class_name = get_new_name(file)
        # Create the label file path
        create_label_file(image_name, sub_path, class_name, train_path / "labels")
        # Copy the image file to the train directory
        shutil.copy(str(file), str(train_path / "images" /  f"{class_name}_{sub_path}_{image_name}.jpg"))

    for file in val_files:
        image_name, sub_path, class_name = get_new_name(file)
        # Create the label file for the image
        create_label_file(image_name, sub_path, class_name, val_path / "labels")
        # Copy the image file to the val directory
        shutil.copy(str(file), str(val_path / "images" /  f"{class_name}_{sub_path}_{image_name}.jpg"))

    for file in test_files:
        image_name, sub_path, class_name = get_new_name(file)
        create_label_file(image_name, sub_path, class_name, test_path / "labels")
        # Copy the image file to the test directory
        shutil.copy(str(file), str(test_path / "images" /  f"{class_name}_{sub_path}_{image_name}.jpg"))

if __name__ == "__main__":
    # Prepare the dataset
    prepare_dataset(train_ratio=0.7, val_ratio=0.15, balance=True)
    print("Dataset prepared successfully.")

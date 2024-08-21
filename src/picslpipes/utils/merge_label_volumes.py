import argparse
import os
import sys
import logging
import SimpleITK as sitk
import numpy as np
import json

def merge_label_volumes( inputs: dict, priorities: list) -> tuple:
    
    """
    Merges label volumes from multiple files into a single volume, resolving overlaps using priorities,
    and generates a JSON metadata file with combined segment information.

    Parameters:
    inputs (dict): Dictionary where keys are labels and values are the corresponding SimpleITK images.
    priorities (list): List of labels in the order of their priority. Higher priority labels appear first.

    Returns:
    tuple: Merged SimpleITK label image and a JSON metadata file as a string.
    """
    
    logging.debug("merge_label_volumes: start")
    
    # Initialize an empty array with the same size as the input images
    first_image = next(iter(inputs.values()))
    #size = first_image.GetSize()
    size = sitk.GetArrayViewFromImage(first_image).shape

    merged_array = np.zeros(size, dtype=np.uint8)  # Assuming label values are integers
    
    # Metadata dictionary to store combined segment information
    metadata = {
        "MergedSegments": []
    }
    
    # Iterate over the priority list to overlay each label and build the metadata
    for priority, label in enumerate(priorities, start=1):
        if label in inputs:
            logging.debug(f"Merging label {label} with priority.")
            label_image = sitk.GetArrayFromImage(inputs[label])

            # Overlay this label on the merged array, prioritizing the current label over the existing one
            merged_array = np.where(label_image > 0, priority, merged_array)

            # Add segment information to the metadata
            metadata["MergedSegments"].append({
                "OriginalLabel": label,
                "Priority": priority,
                "RelabeledValue": priority
            })

    merged_image = sitk.GetImageFromArray(merged_array)
    merged_image.CopyInformation(first_image)

    return((merged_image, metadata))

def main():

    
    # Convert the merged array back to a SimpleITK image
    merged_image = sitk.GetImageFromArray(merged_array)
    merged_image.CopyInformation(first_image)  # Copy spatial information from the original image

    # Convert the metadata dictionary to a JSON string
    metadata_json = json.dumps(metadata, indent=4)

    out_imgs = (merged_image, metadata_json)

    logging.debug("merge_label_volumes: complete")    

    return out_imgs

def get_priority_mapping():
    # This could be replaced with any method to fetch or define priorities
    return {
        'LUNG1-001_09-18-2008-StudyID-NA-69331_seg-1.nii.gz': 3,
        'LUNG1-001_09-18-2008-StudyID-NA-69331_seg-2.nii.gz': 1,
        'LUNG1-001_09-18-2008-StudyID-NA-69331_seg-3.nii.gz': 4,
        'LUNG1-001_09-18-2008-StudyID-NA-69331_seg-4.nii.gz': 2,
    }

def main():
    my_parser = argparse.ArgumentParser(description='Merge labels from multiple files')
    my_parser.add_argument('-i', '--input', type=str, required=True, help="json with files and labels")
    my_parser.add_argument('-p', '--priority', type=str, required=False, help="mapping from priority to label number")
    my_parser.add_argument('-o', '--output', type=str, help="output image filename", required=True) 
    my_parser.add_argument('--verbose', help="Enable verbose output", action='store_true', default=False)

    args = my_parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING, format="%(asctime)s %(name)s - %(levelname)-6s - %(message)s")

    with open(args.input, 'r') as f:
        in_files = json.load(f)
        f.close()

    priority={}
    for count,label in enumerate(in_files.keys()):
        priority[count+1]=label

    if args.priority is not None:
        with open(args.priority) as f:
            priority = json.load(f)
    
    priority_values = list(priority.keys())
    priority_labels = list(priority.values())
    priority_labels.sort(key=lambda x: priority_values)


    in_images = {}
    print(in_files)
    for label, file_path in in_files.items():
        try:
            in_images[label] = sitk.ReadImage(file_path)
        except Exception as e:
            logging.error(f"Could not read input file: {file_path} due to {e}")
            exit(1)

    print(in_images)

    out_imgs = merge_label_volumes(in_images, priority_labels)
    print(out_imgs[1])
    sitk.WriteImage(out_imgs[0], args.output)



if __name__ == "__main__":
    sys.exit(main())
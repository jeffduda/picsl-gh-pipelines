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
    size = first_image.GetSize()
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
    
    # Convert the merged array back to a SimpleITK image
    merged_image = sitk.GetImageFromArray(merged_array)
    merged_image.CopyInformation(first_image)  # Copy spatial information from the original image

    # Convert the metadata dictionary to a JSON string
    metadata_json = json.dumps(metadata, indent=4)

    out_imgs = (merged_image, metadata_json)

    logging.debug("merge_label_volumes: complete")    

    return out_imgs


def main():
    
    my_parser = argparse.ArgumentParser(description='Merge labels from multiple files')
    my_parser.add_argument('--base_path', type=str, required=True, help="Base directory for the segmentation files")
    my_parser.add_argument('--patient_id', type=str, required=True, help="Patient ID")
    my_parser.add_argument('--verbose', help="Enable verbose output", action='store_true', default=False)
    args = my_parser.parse_args()

    # Setup logging
    log_level=logging.WARNING
    if args.verbose:
        log_level=logging.DEBUG
    logging.basicConfig(level=log_level, format="%(asctime)s %(name)s - %(levelname)-6s - %(message)s")

    # Construct the path to the patient's folder
    patient_folder = os.path.join(args.base_path, args.patient_id)

    # Find all segmentation files for this patient
    seg_files = [f for f in os.listdir(patient_folder) if f.endswith('.nii.gz') and 'seg' in f]
    
    # Sort the files to ensure correct order (optional, if the order is important)
    seg_files.sort()

    # Create the input dictionary and priorities list
    in_files = {}
    priorities = []

    for i, seg_file in enumerate(seg_files):
        label = i + 1  # Assuming label IDs start at 1
        in_files[label] = os.path.join(patient_folder, seg_file)
        priorities.append(label)

    # Try to read in all input images
    in_images = {}
    for label, file_path in in_files.items():
        logging.debug("Label " + str(label) + " image: " + file_path)
        try:
            in_images[label] = sitk.ReadImage(file_path)
        except:
            logging.error("Could not read input file: " + file_path)
            exit(1)

    # Do the merge
    out_imgs = merge_label_volumes(in_images, priorities)

    # Define output file paths
    output_image_path = os.path.join(patient_folder, f'{args.patient_id}_merged_segmentation.nii.gz')
    output_metadata_path = os.path.join(patient_folder, f'{args.patient_id}_merged_segmentation_metadata.json')

    # Write outputs to file
    if out_imgs[0] is not None:
        sitk.WriteImage(out_imgs[0], output_image_path)

    if out_imgs[1] is not None:
        with open(output_metadata_path, 'w') as f:
            f.write(out_imgs[1])

    print(f"Merged segmentation and metadata saved for {args.patient_id}.")


if __name__=="__main__":
    sys.exit(main())


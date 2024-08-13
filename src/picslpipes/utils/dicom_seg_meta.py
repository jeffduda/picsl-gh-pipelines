import argparse
import os
import sys
import logging
import pathlib
import pydicom
import json
from typing import Optional

def dicom_seg_meta_dcm( infile: str ) -> dict:
    logging.debug("dicom_seg_meta_dcm: start")
    meta={}
    
    try:
        ds=pydicom.dcmread(infile)
    except:
        logging.error("dicom_seg_meta_dcm: could not read file as dicom: "+infile)
        return None
    


    return(meta)

def dicom_seg_meta_json( infile: str ) -> dict:
    logging.debug("dicom_seg_meta_json: start")
    meta={}

    try:
        file = open(infile, 'r')
        data = json.load(file)
    except:
        logging.error("dicom_seg_meta_json: could not read file as json: "+infile)
        return None       

    return(meta)


def dicom_seg_meta( infile: str ) -> dict:
    
    logging.debug("dicom_seg_meta: start")

    # Check if input path exists
    if not os.path.exists(infile):
        logging.error("dicom_seg_meta: input file does not exist")
        return None

    if pathlib.Path(infile).suffix == ".json":
        meta=dicom_seg_meta_json(infile)
    elif pathlib.Path(infile).suffix == ".dcm":
        meta=dicom_seg_meta_dcm(infile)
    elif pathlib.Path(infile).suffix == "":    
        meta=dicom_seg_meta_json(infile)
    else:
        logging.error("dicom_seg_meta: unknown input file type: "+pathlib.Path(infile).suffix)
        return None

    return(meta)

def dicom_seg_meta(structure_names: list[str], json_path: str) -> dict[str, Optional[int]]:
    '''
    Inputs:
    - structure_names: List of names of desired anatomical structures to be identified from the segmentation
    - json_path: Path to the JSON file that contains the mapping from name to

    Outputs:
    Dictionary where keys are the desired structure names and values are the corresponding label IDs, or None if the structure
    is not present in the segmentation
    '''
    # Load the JSON file
    with open(json_path, 'r') as f:
        label_mapping_data = json.load(f)

    # Initialize the output dictionary
    structure_label_mapping = {structure: None for structure in structure_names}

    # Extract label mappings from the JSON
    for segment in label_mapping_data["segmentAttributes"]:
        for attr in segment:
            segment_description = attr["SegmentDescription"]
            label_id = attr["labelID"]

            # Check if the current segment matches one of the desired structures
            if segment_description in structure_names:
                structure_label_mapping[segment_description] = label_id

    return structure_label_mapping

def main():
    
    my_parser = argparse.ArgumentParser(description='Extract meta info from dicom seg or json')
    my_parser.add_argument('-i', '--input',  type=str, help='json file to get info from', required=True)
    my_parser.add_argument('-o', '--output', type=str, help="file for output", required=True)
    my_parser.add_argument('-s', '--structures', type=str, nargs='+', help="List of structures to identify",
                           required=True)
    my_parser.add_argument('-v', '--verbose', help="verbose output", action='store_true', default=False)
    args = my_parser.parse_args()

    # Setup logging
    log_level=logging.WARNING
    if args.verbose:
        log_level=logging.DEBUG
    logging.basicConfig(level=log_level, format="%(asctime)s %(name)s - %(levelname)-6s - %(message)s")

    logging.debug("Input file: "+str(args.input))

    meta = dicom_seg_meta(args.structures, args.input)
    print(meta)

if __name__=="__main__":
    sys.exit(main())


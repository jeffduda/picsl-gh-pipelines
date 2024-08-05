import argparse
import os
import sys
import logging
import pathlib
import pydicom
import json

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

def main():
    
    my_parser = argparse.ArgumentParser(description='Extract meta info from dicom seg or json')
    my_parser.add_argument('-i', '--input',  type=str, help='file to get info from', required=True)
    my_parser.add_argument('-o', '--output', type=str, help="csv file for output", required=True)
    my_parser.add_argument('-v', '--verbose', help="verbose output", action='store_true', default=False)
    args = my_parser.parse_args()

    # Setup logging
    log_level=logging.WARNING
    if args.verbose:
        log_level=logging.DEBUG
    logging.basicConfig(level=log_level, format="%(asctime)s %(name)s - %(levelname)-6s - %(message)s")


    logging.debug("Input file: "+str(args.input))

    meta = dicom_seg_meta( args.input )
    print(meta)

if __name__=="__main__":
    sys.exit(main())


import argparse
import os
import sys
import glob
import logging

def dicom_seg_files( dir: str, labels: list[int], ext=".nii.gz" ) -> dict:
    
    logging.debug("dicom_seg_files: start")

    # Check if input path exists
    if not os.path.exists(dir):
        logging.error("dicom_seg_files: input directory does not exist")
        return None
    
    # Check that labels were input
    if not len(labels) > 0:
        logging.error("dicom_seg_files: no labels in list")
        return None
    
    
    files={}
    # Find files and put into a dict that looks like:
    # files = { 1:'file_seg-1.nii.gz', 2: 'file_seg-2.nii.gz'}
    
    """
    pass in a directory, match the segments to a dictionary

    have a script that works on every study
    """

    for label in labels:
        my_glob = glob.glob(f"{dir}*seg-{label}{ext}")
        if len(my_glob) == 1:
            files[label] = my_glob[0]

    return(files)

def main():
    
    my_parser = argparse.ArgumentParser(description='Find files for segmentation labels')
    my_parser.add_argument('-d', '--directory',  type=str, help='input directory', required=True)
    my_parser.add_argument('-l', '--labels', type=int, help="label to find image for", required=True, nargs='+')
    my_parser.add_argument('-v', '--verbose', help="verbose output", action='store_true', default=False)
    args = my_parser.parse_args()

    # Setup logging
    log_level=logging.WARNING
    if args.verbose:
        log_level=logging.DEBUG
    logging.basicConfig(level=log_level, format="%(asctime)s %(name)s - %(levelname)-6s - %(message)s")


    logging.debug("Directory to search: "+str(args.directory))
    logging.debug("Labels to find images for: "+str(args.labels))

    files = dicom_seg_files( args.directory, args.labels )
    print(files)

if __name__=="__main__":
    sys.exit(main())


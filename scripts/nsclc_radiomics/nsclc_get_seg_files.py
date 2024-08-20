import os
import sys
import json
import argparse
import glob

def main():

    my_parser = argparse.ArgumentParser(description='Merge labels from multiple files')
    my_parser.add_argument('-d', '--dir', type=str, required=True, help="Base directory for the segmentation files")
    my_parser.add_argument('-i', '--input', type=str, required=True, help="name and labels mapping file")
    my_parser.add_argument('-o', '--o', type=str, required=True, help="file with labels to merge")    
    my_parser.add_argument('--verbose', help="Enable verbose output", action='store_true', default=False)
    args = my_parser.parse_args()

    with open(args.input) as f:
        label_map = json.load(f)
        f.close()

    out_map={}
    
    for k in label_map.keys():
        label = label_map[k]
        seg_file = glob.glob(os.path.join(args.dir, f'*_seg-{k}.nii.gz'))
        out_map[seg_file] = label

    with open(args.output, 'w') as of:
        json.dump(out_map, of)
        of.close()

if __name__ == "__main__":
    sys.exit(main())
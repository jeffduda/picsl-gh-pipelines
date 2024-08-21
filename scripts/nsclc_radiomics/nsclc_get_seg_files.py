import os
import sys
import json
import argparse
import glob

def main():

    my_parser = argparse.ArgumentParser(description='Merge labels from multiple files')
    my_parser.add_argument('-d', '--dir', type=str, required=True, help="Base directory for the segmentation files")
    my_parser.add_argument('-i', '--input', type=str, required=True, help="name and labels mapping file")
    my_parser.add_argument('-o', '--output', type=str, required=True, help="file with labels to merge")    
    my_parser.add_argument('--verbose', help="Enable verbose output", action='store_true', default=False)
    args = my_parser.parse_args()

    out_labels = {"Lung-Left": 1, "Lung-Right": 2}

    with open(args.input) as f:
        label_map = json.load(f)
        f.close()

    out_map={}

    for k in label_map.keys():
        label = label_map[k]
        seg_file = glob.glob(os.path.join(args.dir, '*_seg-'+str(label)+'.nii.gz'))
        out_label = out_labels[k]
        out_map[out_label] = seg_file[0]

    with open(args.output, 'w') as of:
        json.dump(out_map, of)
        of.close()

if __name__ == "__main__":
    sys.exit(main())
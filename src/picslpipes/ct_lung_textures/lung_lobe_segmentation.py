import os
import argparse
import ants
import antspynet
import tensorflow as tf
import sys
import nibabel as nib
from totalsegmentator.python_api import totalsegmentator


def totalsegmentator_lung_vessels(img: str, mask: str, out_file: str, verbose=False):
    ct = nib.load(img)
    vessel_seg = totalsegmentator(ct, task='lung_vessels')
    nib.save(vessel_seg, out_file)

    vessel_img = ants.image_read(out_file)
    vessel_img = ants.threshold_image(vessel_img,1,1,1,0)

    if mask is not None:
        mask_img = ants.image_read(mask)
        mask_img = ants.threshold_image(mask_img, 0, 0, 0, 1)
        vessel_img = mask_img * vessel_img
    
    ants.image_write(vessel_img, out_file)
    

def ants_lung_extraction(img: str, out_file: str, verbose=False):
    """
    Extract the lung lobes from a binary mask using ANTs
    :param mask: input binary mask
    :param out_file: output mask
    :return: None
    """
    ct = ants.image_read(img)
    lung_ex = antspynet.lung_extraction(ct, modality="ct", verbose=verbose)

    out_mask = lung_ex['segmentation_image']*0
    lung_left = ants.threshold_image(lung_ex['segmentation_image'], 1, 1, 1, 0)
    left_cluster = ants.iMath(lung_left, 'GetLargestComponent', 20)
    #ants.image_write(left_cluster, 'left_cluster.nii.gz')
    out_mask[left_cluster > 0] = 1
    lung_right = ants.threshold_image(lung_ex['segmentation_image'], 2, 2, 1, 0)
    right_cluster = ants.iMath(lung_right, 'GetLargestComponent', 20)
    #ants.image_write(right_cluster, 'right_cluster.nii.gz')
    out_mask[right_cluster > 0] = 2
    ants.image_write(out_mask, out_file)

def ants_lung_lobes_from_mask(mask: str, out_file: str, verbose=False):
    """
    Extract the lung lobes from a binary mask using ANTs
    :param mask: input binary mask
    :param out_file: output mask
    :return: None
    """
    mask_img = ants.image_read(mask)
    mask_img = ants.threshold_image(mask_img, 0, 0, 0, 1)
    lung_ex = antspynet.lung_extraction(mask_img, modality="maskLobes", verbose=verbose)
    out_img = lung_ex['segmentation_image'] * mask_img
    ants.image_write(out_img, out_file)

def main():
    parser = argparse.ArgumentParser(description='Apply lung segmentation models to a CT volume')
    parser.add_argument('-i', '--input', help='Input CT volume', type=str, required=True)
    parser.add_argument('-x', '--mask', help='Mask to use for segmentation', type=str, required=False)
    parser.add_argument('-m', '--model', help='Model to use for segmentation', type=str, required=True)
    parser.add_argument('-o', '--output', help='Output volume')
    args = parser.parse_args()
    print(args)

    if args.model=='ants_lung':
        print("runnning... ants lung extraction")
        print("input: ", args.input)
        print("output: ", args.output)
        ants_lung_extraction(args.input, args.output, verbose=True)
    elif args.model=='ants_lobes':
        print("runnning... ants lobe extraction")
        print("input: ", args.input)
        print("output: ", args.output)
        ants_lung_lobes_from_mask(args.input, args.output, verbose=True)
    elif args.model=='ts_vessels':
        print("runnning... total segmentator lung vessels")
        print("input: ", args.input)
        print("output: ", args.output)
        totalsegmentator_lung_vessels(args.input, args.mask, args.output)
    else:
        print("Model not recognized. Choose from [ants_lung, ants_lobes]")
        exit(1)


if __name__=="__main__":
    sys.exit(main())


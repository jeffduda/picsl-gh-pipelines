import argparse
import os
import sys
import logging
import SimpleITK as sitk

def merge_label_volumes( inputs: dict ) -> tuple:
    
    logging.debug("merge_label_volumes: start")
    
    out_imgs=(None,None)

    segmentations = []
    segmentation_arrays = []

    for d, dirname in enumerate(glob.glob(my_dir + r"/NSCLC-Radiomics-recon/LUNG1-*")):
        segmentations.append([sitk.ReadImage(os.path.join(dirname, file)) for file in glob.glob(dirname + r"/*/*seg-*.nii.gz")])
        segmentation_arrays.append([sitk.GetArrayFromImage(seg)[:,::-1,:] for seg in segmentations[d]])

        combined_segmentation_overlap_array = sitk.GetArrayFromImage(sitk.Image(segmentations[d][0].GetSize(), sitk.sitkUInt8))

        combined_segmentation_array = segmentation_arrays[d][0]
        for segmentation_array in segmentation_arrays[d][1:]:
            combined_segmentation_overlap_array[np.logical_and(segmentation_array!=0, combined_segmentation_array!=0)] = segmentation_array[np.logical_and(segmentation_array!=0, combined_segmentation_array!=0)] + combined_segmentation_array[np.logical_and(segmentation_array!=0, combined_segmentation_array!=0)]
            combined_segmentation_array[segmentation_array!=0] = segmentation_array[segmentation_array!=0]
        
        combined_segmentation = sitk.GetImageFromArray(combined_segmentation_array.astype(np.uint8))
        combined_segmentation.CopyInformation(segmentations[d][0])

        combined_segmentation_overlap = sitk.GetImageFromArray(combined_segmentation_overlap_array.astype(np.uint8))
        combined_segmentation_overlap.CopyInformation(segmentations[d][0])

    out_imgs = (combined_segmentation, combined_segmentation_overlap)
    return(out_imgs)

def main():
    
    my_parser = argparse.ArgumentParser(description='Merge labels from multiple files')
    my_parser.add_argument('-i', '--input', type=str, help="label to find image for", required=True, nargs=2, action='append')
    my_parser.add_argument('-o', '--output', type=str, help="verbose output", required=True, nargs=2)
    my_parser.add_argument('-v', '--verbose', help="verbose output", action='store_true', default=False)
    args = my_parser.parse_args()
    print(args)

    # Setup logging
    log_level=logging.WARNING
    if args.verbose:
        log_level=logging.DEBUG
    logging.basicConfig(level=log_level, format="%(asctime)s %(name)s - %(levelname)-6s - %(message)s")


    # Check inputs for valid labels
    in_files={}
    for input in args.input:
        if input[1] in in_files:
            logging.error("Each image must have a unique label value")
            exit(1)
        in_files[input[1]]=input[0]

    # Try to read in all input images
    in_images={}
    for k in in_files.keys():
        logging.debug("Label " +str(k) + " image: "+in_files[k])
        try:
            in_images[k]=sitk.ReadImage(in_files[k])
        except:
            logging.error("could not read input file: "+in_files[k])
            exit(1)

    # Do the merge
    out_imgs = merge_label_volumes( in_images )

    # Write outputs to file
    if out_imgs[0] is not None:
        sitk.WriteImage(out_imgs[0], args.output[0] )

    if out_imgs[1] is not None:
        sitk.WriteImage(out_imgs[1], args.output[1] )

if __name__=="__main__":
    sys.exit(main())


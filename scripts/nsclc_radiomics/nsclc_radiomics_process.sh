#!/bin/bash
input_dir=$1
output_dir=$2

module load python
py_path="/home/jtduda/pkg/picsl-gh-pipelines/src/picslpipes/utils"

# Find the file with info on the segmentation labels
meta_file=$(ls ${input_dir}/*seg-meta.json)
python $py_path/dicom_seg_meta.py -i $meta_file -o ${out_dir}/seg_labels.json -s Lung_Left Lung_Right



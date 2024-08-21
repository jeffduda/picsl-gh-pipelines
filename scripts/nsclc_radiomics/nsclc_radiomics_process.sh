#!/bin/bash
input_dir=$1
out_dir=$2

source /project/picsl/jtduda/lung_sarg/bin/activate
module load ANTs

py_path="/home/jtduda/pkg/picsl-gh-pipelines/src/picslpipes/utils"
scripts="/home/jtduda/pkg/picsl-gh-pipelines/scripts/nsclc_radiomics"
lung_path="/home/jtduda/pkg/picsl-gh-pipelines/src/picslpipes/ct_lung_textures"

if [ ! -e "$out_dir" ]; then
  mkdir -p $out_dir
fi

# Find the file with info on the segmentation labels
meta_file=$(ls ${input_dir}/*seg-meta.json)
ct_file=$(ls ${input_dir}/*CT.nii.gz)
name=$(basename $ct_file .nii.gz)

session=$(basename $input_dir)
dir=$(dirname $input_dir)
sub=$(basename $dir)

echo "subject: $sub"
echo "session: $session"
echo "meta file: $meta_file"

echo "Prepare manual lung segmentation"
#python ${py_path}/dicom_seg_meta.py -i $meta_file -o ${out_dir}/${name}_seg_labels.json -s Lung-Left Lung-Right
#python ${scripts}/nsclc_get_seg_files.py -d $input_dir -i ${out_dir}/${name}_seg_labels.json -o ${out_dir}/${name}_seg_files.json
#python ${py_path}/merge_label_volumes.py -i ${out_dir}/${name}_seg_files.json -o ${out_dir}/${name}_lungs.nii.gz
#ThresholdImage 3 ${out_dir}/${name}_lungs.nii.gz ${out_dir}/${name}_lung_mask.nii.gz 1 2 1 0

#echo "Auto segment lung lobes"
#python ${lung_path}/lung_lobe_segmentation.py -i ${out_dir}/${name}_lung_mask.nii.gz -o ${out_dir}/${name}_lung_lobes.nii.gz -m ants_lobes
#python ${lung_path}/lung_lobe_segmentation.py -i $ct_file -o ${out_dir}/${name}_ants_lungs.nii.gz -m ants_lung
#ThresholdImage 3 ${out_dir}/${name}_ants_lungs.nii.gz ${out_dir}/${name}_ants_lung_mask.nii.gz 1 2 1 0
#python ${lung_path}/lung_lobe_segmentation.py -i ${out_dir}/${name}_ants_lung_mask.nii.gz -o ${out_dir}/${name}_ants_lung_lobes.nii.gz -m ants_lobes

echo "Segment lung vessels"
#python ${lung_path}/lung_lobe_segmentation.py -i $ct_file -o ${out_dir}/${name}_lung_vessels.nii.gz -m ants_lung -x ${out_dir}/${name}_lung_mask.nii.gz

echo "Segment all structs"
#TotalSegmentator -i $ct_file -o ${out_dir}/${name}_ts.nii.gz --ml --task total

# Extract totalsegmentator lung lobes
#ThresholdImage 3 ${out_dir}/${name}_ts.nii.gz ${out_dir}/tmp_lobe1.nii.gz 11 11 1 0
#ThresholdImage 3 ${out_dir}/${name}_ts.nii.gz ${out_dir}/tmp_lobe2.nii.gz 10 10 2 0
#ThresholdImage 3 ${out_dir}/${name}_ts.nii.gz ${out_dir}/tmp_lobe3.nii.gz 14 14 3 0
#ThresholdImage 3 ${out_dir}/${name}_ts.nii.gz ${out_dir}/tmp_lobe4.nii.gz 13 13 4 0
#ThresholdImage 3 ${out_dir}/${name}_ts.nii.gz ${out_dir}/tmp_lobe5.nii.gz 12 12 5 0
#ImageMath 3 ${out_dir}/${name}_ts_lung_lobes.nii.gz + ${out_dir}/tmp_lobe1.nii.gz ${out_dir}/tmp_lobe2.nii.gz
#ImageMath 3 ${out_dir}/${name}_ts_lung_lobes.nii.gz + ${out_dir}/${name}_ts_lung_lobes.nii.gz ${out_dir}/tmp_lobe3.nii.gz
#ImageMath 3 ${out_dir}/${name}_ts_lung_lobes.nii.gz + ${out_dir}/${name}_ts_lung_lobes.nii.gz ${out_dir}/tmp_lobe4.nii.gz
#ImageMath 3 ${out_dir}/${name}_ts_lung_lobes.nii.gz + ${out_dir}/${name}_ts_lung_lobes.nii.gz ${out_dir}/tmp_lobe5.nii.gz
#ThresholdImage 3 ${out_dir}/${name}_ts_lung_lobes.nii.gz ${out_dir}/tmp_left.nii.gz 1 2 1 0
#ThresholdImage 3 ${out_dir}/${name}_ts_lung_lobes.nii.gz ${out_dir}/tmp_right.nii.gz 3 5 2 0
#ImageMath 3 ${out_dir}/${name}_ts_lungs.nii.gz + ${out_dir}/tmp_left.nii.gz ${out_dir}/tmp_right.nii.gz
#ThresholdImage 3 ${out_dir}/${name}_ts_lungs.nii.gz ${out_dir}/${name}_lung_mask.nii.gz 0 0 0 1
#rm ${out_dir}/tmp*.nii.gz

# Texture maps


# Get stats files
python $py_path/image_region_stats.py -i $ct_file -s ${out_dir}/${name}_lung_lobes.nii.gz -k /project/picsl/jtduda/GlobalHealth/data/NSCLC-Radiomics/info/lobe_key.csv -n manual-lobes -o ${out_dir}/${name}_lung_lobes_sitk.csv -a $sub -b $session
python $py_path/image_region_stats.py -i $ct_file -s ${out_dir}/${name}_lungs.nii.gz -k /project/picsl/jtduda/GlobalHealth/data/NSCLC-Radiomics/info/lung_key.csv -n manual-lungs -o ${out_dir}/${name}_lungs_sitk.csv -a $sub -b $session









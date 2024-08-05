# Global Lung Health
Cloud-based framework for lung health monitoring

# Getting started with Lung CT images

1. Cleaning and prepping data
    1. Data formats
        1. Dicom
        2. DicomSeg
        3. Nifti
    2. Viewing images with itksnap
    3. Conversion tools
        1. dcm2niix for dicom image to nifti
        2. dcmqi for dicom seg to nifti
        3. ANTs to correct for variation in voxel ordering

## Meeting briefs
- 7.18.24: Discussed possible sources of data to start with. We decided to use some sample data from TCIA while waiting to see if some on-site sample data was available. I asked to install SimpleITK for python and itksnap. A few days later I sent out a link to 10 sample datasets that had dicom and dicom seg files. I wrote a script to convert those to nifti volumes and included the script and reconstructions in the shared folder. Next steps:
    - View a CT lung image and associated segmentatation labels in itk-snap. Pull up label statistics for those labels
    - Open image volumes using SimpleITK
- 7.23.24: Went over the reconstructions of the sample data. Looking at the meta data in the json, we realized that associations between label number and anatomical structure vary per subjects so we need write some code to create image volume with consistent label numberings. Next steps:
    - Write code to parse json files to get label number to anatomy mapping
    - Write code to pull out left lung, right lung and spinal cord to create a merged label volume
    - Make sure to watchout for possible double-labels when merging 
- 8.1.24: Gave overview of future steps leading up to evaluating models and collecting texture features in the lung. Next steps:
    - Finalize scripts for extracting info from json files and merging lung labels
    - Use 1=LeftLung and 2=RightLung to make later comparisons easier
    - Forgot to mention - Use connected components to "clean" labels
    - For label merging, create a map for "double-labeled" voxels
    - Attempt to run SimpleITK filter: LabelShapeStatisticsImageFilter()
    - Collect statistics into a long-format csv for each image volume
    - Looking at the data in R. Basic summary stats and plotting with ggplot2




# Background

## Lung Cancer in Nigeria
Description of the problem with relevant references

## Regulatory considerations
Summary of the issue to be considered with references

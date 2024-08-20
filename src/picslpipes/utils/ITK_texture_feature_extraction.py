#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 17:55:27 2024

@author: mariamrizvi
"""

import itk

def compute_texture_features(input_image_path, output_image_path):
    # Read the input image
    image = itk.imread(input_image_path, itk.F)

    # Setup the texture features filter
    texture_filter = itk.ScalarImageToTextureFeaturesImageFilter.New(image)
    texture_filter.SetNumberOfBinsPerAxis(256)
    texture_filter.SetPixelValueMinMax(0, 255)
    texture_filter.SetNeighborhoodRadius([2, 2, 2])
    
    # Optional: Setup additional configuration for texture_filter if needed

    # Execute the texture features filter
    texture_feature_image = texture_filter.GetOutput()
    
    # Setup the run length features filter
    run_length_filter = itk.ScalarImageToRunLengthFeaturesImageFilter.New(image)
    run_length_filter.SetNumberOfBinsPerAxis(256)
    run_length_filter.SetPixelValueMinMax(0, 255)
    run_length_filter.SetDistanceValueMinMax(0, 10)  # Example values
    run_length_filter.SetNeighborhoodRadius([2, 2, 2])
    
    # Optional: Setup additional configuration for run_length_filter if needed

    # Execute the run length features filter
    run_length_feature_image = run_length_filter.GetOutput()

    # Write output - separate files for texture and run length features
    itk.imwrite(texture_feature_image, 'texture_' + output_image_path)
    itk.imwrite(run_length_feature_image, 'run_length_' + output_image_path)

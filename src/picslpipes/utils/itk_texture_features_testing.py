import itk
import numpy as np
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Apply lung segmentation models to a CT volume')
    parser.add_argument('-i', '--input', help='Input CT volume', type=str, required=True)
    parser.add_argument('-s', '--seg', help='Input segmentation', type=str, required=True)
    parser.add_argument('-n', '--min', help='Minimum intensity value', type=int)
    parser.add_argument('-x', '--max', help='Maximum intensity value', type=int)
    parser.add_argument('-b', '--bins', help='Number of bins per axis', type=int, default=None)
    parser.add_argument('-f', '--features', help='Type of features to calculate: GLCM or GLRLM', type=str, default='GLCM')
    parser.add_argument('-d', '--min_distance', help='Distance value min', type=int)
    parser.add_argument('-e', '--max_distance', help='Distance value max', type=int)
    parser.add_argument('-m', '--meta', help="subject info" , type=str, default="")
    parser.add_argument('-k', '--key_meta', help="subject info key" , type=str, default="")
    parser.add_argument('-a', '--attenuation', help='attenuation stats', type=bool, default=False)

    args = parser.parse_args()

    image = itk.imread(args.input, itk.ctype('float'))
    mask = itk.imread(args.seg, itk.ctype('float'))

    #rescaler = itk.RescaleIntensityImageFilter.New(image)
    #rescaler.SetOutputMinimum(0)
    #rescaler.SetOutputMaximum(255)
    #rescaler.Update()
    #image = rescaler.GetOutput()
    #image = itk.add_image_filter(image,1024)


    texture_filter = None
    names = None
    if args.features == "GLCM":
        texture_filter = itk.ScalarImageToTextureFeaturesFilter.New(image)
        
        names = ["Energy", "Entropy", "InverseDifferenceMoment", "Inertia", "ClusterShade", "ClusterProminence","Correlation","HaralickCorrelation"]
        features = texture_filter.GetRequestedFeatures()
        features.CreateElementAt(6)
        features.SetElement(6,2)
        features.CreateElementAt(7)
        features.SetElement(7,7)
        texture_filter.SetRequestedFeatures(features)

    if args.features == "GLRLM":
        texture_filter = itk.ScalarImageToRunLengthFeaturesFilter.New(image)
        texture_filter.SetDistanceValueMinMax(1,20)

        features = texture_filter.GetRequestedFeatures()
        names = ["ShortRunEmphasis", "LongRunEmphasis", "GreyLevelNonuniformity", "RunLengthNonuniformity", "LowGreyLevelRunEmphasis", "HighGreyLevelRunEmphasis", "ShortRunLowGreyLevelEmphasis", "ShortRunHighGreyLevelEmphasis", "LongRunLowGreyLevelEmphasis", "LongRunHighGreyLevelEmphasis"]  

    if texture_filter is None:
        print("Invalid feature type")
        return(1)

    texture_filter.SetMaskImage(mask)

    imin = args.min
    imax = args.max

    if (imin is None) or (imax is None):
        range_filter = itk.MinimumMaximumImageFilter.New(image)
        range_filter.Update()

        if imin is None:
            imin = range_filter.GetMinimum()
        if imax is None:
            imax = range_filter.GetMaximum()

    nbins = args.bins
    if nbins is None:
        nbins = int(imax-imin+1)

    texture_filter.SetNumberOfBinsPerAxis(nbins)
    texture_filter.SetPixelValueMinMax(imin,imax)

    

    stats_filt = itk.LabelStatisticsImageFilter.New(image)
    stats_filt.SetLabelInput(mask.astype(itk.UC))
    stats_filt.Update()

    labels = np.sort(np.unique(itk.array_view_from_image(mask)))
    labels = [int(x) for x in labels if x != 0]
    #print(labels)
    #print(names)

    voxvol=np.prod(image.GetSpacing())

    if not args.key_meta is "":
        print(args.key_meta+",Calculator,Label,Type,Measure,Metric,Value")

    for v in labels:
        
        texture_filter.SetInsidePixelValue(v)
        texture_filter.Update()
        #print("label: " + str(v))
        #print( "vox count: " + str(stats_filt.GetCount(v)))
        means = texture_filter.GetFeatureMeans()
        sd = texture_filter.GetFeatureStandardDeviations()
        #print("Number of features: " + str(means.Size()))
        for i in range(0, means.Size()):
            print(args.meta+",ITK,"+str(v)+","+args.features+","+names[i] + ",Mean," + str(means.GetElement(i)))
            print(args.meta+",ITK,"+str(v)+","+args.features+","+names[i] + ",StandardDeviation," + str(sd.GetElement(i)))
        if args.attenuation:
            print(args.meta+",Calculator,System,firstorder,"+str(v)+","+"Volume"+"," + str(voxvol*stats_filt.GetCount(v)) + ",NA")
            sd=np.sqrt(stats_filt.GetVariance(v))
            print(args.meta+",ITK,"+str(v)+","+"Mean"+"," + str(stats_filt.GetMean(v)) + "," + str(sd))
            print(args.meta+",ITK,"+str(v)+","+"Maximum"+"," + str(voxvol*stats_filt.GetMaximum(v)) + ",NA")
            print(args.meta+",ITK,"+str(v)+","+"Minimum"+"," + str(voxvol*stats_filt.GetMinimum(v)) + ",NA")
            print(args.meta+",ITK,"+str(v)+","+"Median"+"," + str(voxvol*stats_filt.GetMedian(v)) + ",NA")




    return(0)
if __name__=="__main__":
    sys.exit(main())
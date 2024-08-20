import itk, sys,argparse

def main():
    parser = argparse.ArgumentParser(description='Apply lung segmentation models to a CT volume')
    parser.add_argument('-i', '--input', help='Input CT volume', type=str, required=True)
    parser.add_argument('-s', '--seg', help='Input segmentation', type=str, required=True)
    parser.add_argument('-f', '--features', help='Type of features to calculate: GLCM or GLRLM', type=str, default='GLCM')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-b', '--bins', help='Number of bins per axis', type=int, default=256)
    parser.add_argument('-n', '--min', help='Minimum intensity value', type=int)
    parser.add_argument('-x', '--max', help='Maximum intensity value', type=int)
    parser.add_argument('-r', '--radius', help='Neighborhood radius', type=int, default=2)
    parser.add_argument('-d', '--min-distance', help='Distance value min', type=int)
    parser.add_argument('-e', '--max-distance', help='Distance value max', type=int)
    args = parser.parse_args()
    print(args)

    # Note - input image *must* have integer pixel type

    #Input scan reader
    Dimension = 3
    InputPixelType = itk.ctype('signed short')
    InputImageType = itk.Image[InputPixelType, Dimension]
    imReader = itk.ImageFileReader[InputImageType].New()
    imReader.SetFileName(args.input)

    #Input mask reader
    MaskPixelType = itk.ctype('unsigned char')
    MaskImageType = itk.Image[MaskPixelType, Dimension]
    maskReader = itk.ImageFileReader[MaskImageType].New()
    maskReader.SetFileName(args.seg)

    im = imReader.GetOutput()
    mask = maskReader.GetOutput()

    if args.features == 'GLCM':
        filtr = itk.CoocurrenceTextureFeaturesImageFilter.New(im)
        filtr.SetMaskImage(mask)
        filtr.SetNumberOfBinsPerAxis(args.bins)
        if args.min is not None:
            filtr.SetHistogramMinimum(args.min)
        if args.max is not None:
            filtr.SetHistogramMaximum(args.max)
        filtr.SetNeighborhoodRadius([args.radius, args.radius, args.radius])
        result = filtr.GetOutput()
        itk.imwrite(result, args.output)
    elif args.features == 'GLRLM':
        filtr = itk.RunLengthTextureFeaturesImageFilter.New(im)
        filtr.SetMaskImage(mask)
        filtr.SetNumberOfBinsPerAxis(args.bins)
        if args.min is not None:
            filtr.SetHistogramValueMinimum(args.min)
        if args.max is not None:
            filtr.SetHistogramValueMaximum(args.max)
        if args.min_distance is not None:
            filtr.SetHistogramDistanceMinimum(args.min_distance)
        if args.max_distance is not None:
            filtr.SetHistogramDistanceMaximum(args.max_distance)
        filtr.SetNeighborhoodRadius([args.radius, args.radius, args.radius])
        result = filtr.GetOutput()
        itk.imwrite(result, args.output)
    else:
        print('Unknown feature type')
        return(1)
    
    return(0)
if __name__=="__main__":
    sys.exit(main())
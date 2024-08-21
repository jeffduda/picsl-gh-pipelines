import SimpleITK as sitk
import os, sys, argparse
import csv
import pandas as pd

# id,accession,series_number,series_name,system,label,number,calculator,measure,metric,value
def stats_to_csv(stats, key, sys_name, calc, subject, session):
    dat=[]
    for label in stats.keys():
        istats=stats[label]
        print(label)

        for measure in istats.keys():   
            print(measure)
            mstats=istats[measure]
            for metric in  mstats.keys():
                print(metric)
                row = {"subject": subject, "session": session, "label":label, "name": key[label], "system": sys_name, "measure": measure, "metric": metric, "value": mstats[metric]}
                dat.append(row)
    return(dat)

def get_simple_itk_stats(image, labels, key, extended):

    stats = sitk.LabelIntensityStatisticsImageFilter()
    stats.SetBackgroundValue(0)

    if extended:
        stats.ComputeFeretDiameterOn()
        stats.ComputePerimeterOn()

    stats.Execute(labels, image)
    dat={}
    for value in key:
        intensity={}
        shape={}
        measure={}
        value=int(value)
        if stats.HasLabel(value):
            intensity["mean"] = stats.GetMean(value)
            intensity["minimum"] = stats.GetMinimum(value)
            intensity["maximum"] = stats.GetMaximum(value)
            intensity["median"] = stats.GetMedian(value)
            intensity["sd"] = stats.GetStandardDeviation(value)
            shape["physical_size"] = stats.GetPhysicalSize(value)
            if extended:
                shape["roundness"] = stats.GetRoundness(value)
                shape["skewness"] = stats.GetSkewness(value)
                shape["elongation"] = stats.GetElongation(value)
                shape["feret_diameter"] = stats.GetFeretDiameter(value)
                shape["ellipsoid_diameter_0"] = stats.GetEquivalentEllipsoidDiameter(value)[0]
                shape["ellipsoid_diameter_1"] = stats.GetEquivalentEllipsoidDiameter(value)[1]
                shape["ellipsoid_diameter_2"] = stats.GetEquivalentEllipsoidDiameter(value)[2]
                shape["equivalent_spherical_radius"] = stats.GetEquivalentSphericalRadius(value)
        measure['shape']=shape
        measure['intensity']=intensity
        dat[value]=measure
    return(dat)

def main():
    parser = argparse.ArgumentParser(description='Apply lung segmentation models to a CT volume')
    parser.add_argument('-i', '--input', help='Input CT volume', type=str, required=True)
    parser.add_argument('-s', '--segmentation', help='Labeled regions', type=str, required=True)
    parser.add_argument('-k', '--key', help='csv with labels and names', type=str, required=True)
    parser.add_argument('-n', '--name', help='name of the labeling system', type=str, required=True)
    parser.add_argument('-c', '--calculator', help='package to use for stats: [simpleitk, pyradiomics]', type=str, required=False, default="simpleitk")
    parser.add_argument('-e', '--extended', help='get shape stats', type=bool, required=False, default=True)
    parser.add_argument('-a', '--subject', type=str, required=True)
    parser.add_argument('-b', '--session', type=str, required=True)    

    parser.add_argument('-o', '--output', help='Output csv')
    args = parser.parse_args()

    key={}
    with open(args.key, 'r') as keyfile:
        reader=csv.reader(keyfile)
        for count, row in enumerate(reader):
            if count > 0 and (len(row)>0):
                print(row)
                key[int(row[0])]=row[1]
        keyfile.close()

    print(key)
    
    if args.calculator == 'simpleitk':
        signal = sitk.ReadImage(args.input)
        labels = sitk.ReadImage(args.segmentation, sitk.sitkUInt16)
        stats = get_simple_itk_stats(signal, labels, key, args.extended )
        print(stats)



        dat=stats_to_csv(stats, key, args.name, args.calculator, args.subject, args.session)
        print(dat)
        df=pd.DataFrame(dat)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(df)
        df.to_csv(args.output)


if __name__ == "__main__":
    sys.exit(main())

import archook              
archook.get_arcpy()    
import arcpy                    # loads Arcpy (arcmap's python interface) 
import pandas as pd             # loads pandas (convenient for calculating statistics) 
import os
import numpy as np              # load numpy

arcpy.env.overwriteOutput = True                                                  # Dangerous but avoids issues with overwriting temporary files giving errors
arcpy.CheckOutExtension("Spatial")                                                # checkout the SA extension

inputpolygon="C:/Users/cfassett/Desktop/SashankRedo/Raster_DensInt2_remove.shp"        # polygon file to loop over (i.e., Harry's ages, fishneted)
datafile="S:/Moon/DIVINER_RockAbundances/dgdr_ra_avg_cyl_128_jp2_nulled_scaled_prj.tif"                    # raster data (i.e., rock abundance)
tempfile="C:/cratext/local.tif"                                            #  temporary file
tempshp="C:/cratext/tmp.shp"                                            #  temporary file
arcpy.MakeFeatureLayer_management(inputpolygon, "lyr")                            # creates a 'layer'  (selection will later run on layer, not file)                     

selectnum=int(arcpy.GetCount_management("lyr").getOutput(0))                                        # length 
selectrange=range(selectnum)
#selectrange=range(1) #single example for testing

ofile='sashankredo2.csv'
f=open(ofile, 'a')
f.write('ra,freq\n')
f.close()

for currs in selectrange:
    f=open(ofile, 'a')
    print str(currs) + "/"  + str(selectnum)
    selectcriteria="FID = "+str(currs)                                            # need to have a fid field in the input polygon.  If this doesn't exist, will need to make it.
    arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION",selectcriteria) # select one of the polygons     
    arcpy.CopyFeatures_management("lyr",tempshp)
    arcpy.MakeFeatureLayer_management(tempshp, "templyr")                            # creates a 'layer'  (selection will later run on layer, not file)                     
    LocalRaster = arcpy.sa.ExtractByMask(datafile,"templyr")                                    # extracts the raster at the tempfile pixel (i.e. rock abundance; should have ~400 values)
    rows = arcpy.SearchCursor("lyr")  #get a cursor on the selected shape  to pull out gridcode
    for row in rows:
        gc=row.getValue("gridcode")

    
    
    arr = arcpy.RasterToNumPyArray(LocalRaster).flatten()                            # makes a flattened numpy array (basically a list) of all the values in that extracted rock abundance raster    
    arrm=arr[arr>=0]
    arrmc=np.ma.compressed(arrm)
    gca=int(gc)*np.ones((arrmc.size,1))
    combarray=np.append(arrmc.reshape(arrmc.size,1),gca,axis=1)  # numpy array with results
    np.savetxt(f,combarray, fmt=('%4.3f','%i'),delimiter=',')   
    arcpy.Delete_management("templyr")
    f.close()
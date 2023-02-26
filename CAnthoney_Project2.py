# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:04:59 2021

@author: Cheryl
"""

import arcpy

# Get target folder and find all the vector datasets in it
tf = arcpy.GetParameterAsText(0)
arcpy.env.workspace = tf
fclist = arcpy.ListFeatureClasses()


#Get target projection dataset
tp = arcpy.GetParameterAsText(1)
targetSR = arcpy.Describe(tp).spatialReference

#Create string for geoprocessing message
messageString = "Projected "

try:
    for fc in fclist:
        fcSR = arcpy.Describe(fc).spatialReference
        #Skip projecting any datsets that are already in the target projection
        if fcSR.Name != targetSR.name:
            #Remove .shp
            rootName = fc.replace(".shp","") 
            #Append _projected
            fcFullName = rootName + "_projected.shp"
            #Project the feature classes
            arcpy.management.Project(fc, fcFullName, targetSR)
            # Add datasets to geoprocessing message string
            messageString += fc + ", "
        arcpy.AddMessage(arcpy.GetMessages()) 

    #Remove trailing comma
    messageString = messageString[:-2]
    arcpy.AddMessage(messageString)
    arcpy.AddMessage("All done!")
except:
    arcpy.AddError("Unable to reproject datasets")

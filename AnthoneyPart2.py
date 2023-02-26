# -*- coding: utf-8 -*-
"""
Created on Fri May 21 20:43:39 2021

@author: Cheryl
"""

import arcpy
from arcpy.sa import *

# Specify the input raster
inRaster = "C:/PSU/Geog485/Lesson1/foxlake"

# Check out the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")


try:
    #Create contour lines for the quadrangle
    Contour(inRaster,"C:/PSU/Geog485/Lesson1/outcontour1.shp", 25,0)
    # Report a success message    
    print("Contour successful!")
     
except:
    #Report an error message
    print("Could not complete the contour")
    
try:
    #Calculate slope for the quadrangle
    outSlope = Slope(inRaster, "DEGREE")
    #Save the ouput
    outSlope.save("C:/PSU/Geog485/Lesson1/outslope1")
    print("Slope successful!")

except:
    #Report an error message
    print("Could not complete the slope.")
    
# Check in the Spatial Analyst extension 
arcpy.CheckInExtension("Spatial")
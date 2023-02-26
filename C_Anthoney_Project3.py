# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 17:37:37 2021

@author: Cheryl
"""

import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = "C:\\PSU\\Geog485\\Lesson3"

# Assign parameters

positionsList = ["C", "RW", "LW"]
country = "Sweden"
countryLayer = "Countries_WGS84.shp"
playersLayer = "nhlrosters.shp"
whereClause = "CNTRY_NAME" + "='" + country + "'"

try:
    for p in positionsList:
        #Select country boundary
        countrySelect = arcpy.SelectLayerByAttribute_management(countryLayer, "NEW_SELECTION", whereClause)
        #Select players within country
        playersCountry = arcpy.SelectLayerByLocation_management(playersLayer, "WITHIN", countrySelect)
        #Select players at the desired position and save shapefiles
        whereClause2 = "position" + "='" + p + "'"
        playersCountryPosition = arcpy.SelectLayerByAttribute_management(playersCountry, "SUBSET_SELECTION", whereClause2)
        arcpy.CopyFeatures_management(playersCountryPosition, p)
        #Add the "height_cm" and "weight_kg" fields
        name = p + ".shp"
        arcpy.AddField_management(name, "height_cm", "FLOAT")
        arcpy.AddField_management(name, "weight_kg", "FLOAT")
        #Use UpdateCursor to populate fields with appropriate values
        with arcpy.da.UpdateCursor(name, ("weight", "height","weight_kg", "height_cm")) as cursor:
            for row in cursor:
                #convert weight to kg
                row[2] = int(row[0])*0.453592
                #get height in inches for conversion to cm
                heightSplit=row[1].split("'")
                inches = heightSplit[1]
                inches = inches[:-1]
                inches = (int(heightSplit[0])*12) + int(inches)
                row[3] = inches * 2.54
                cursor.updateRow(row)
        del row, cursor
        arcpy.Delete_management(playersCountryPosition)
        arcpy.Delete_management(countrySelect)
        arcpy.Delete_management(playersCountry)
        print("Successfully created " + p + " shapefile.")
    
except:
    print("Unable to create player shapefiles")
    
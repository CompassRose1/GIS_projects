# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 18:28:36 2021

@author: Cheryl
"""

import arcpy
import csv

arcpy.env.workspace = r"C:\PSU\Geog485\Lesson4"
pointFilePath = arcpy.env.workspace + r"\WakefieldParkRaceway_20160421.csv"

#Create spatial reference object
spatial_ref = arcpy.SpatialReference("WGS 1984")

#Define function for creating polyline
def CreatePolyline(lap):
    out_path = r"C:\PSU\Geog485\Lesson4"
    out_name = str(lap) + "Path.shp"
    geometry_type = "POLYLINE"
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type, "","","", spatial_ref)
    #Add fields for lap number and time
    arcpy.management.AddField(out_name, "Lap", "SHORT")
    arcpy.management.AddField(out_name, "Time", "SHORT")

try:
    #Open and Read csv file
    with open(pointFilePath, "r") as trackPoints:
        csvReader = csv.reader(trackPoints)
        header = next(csvReader)
        latIndex = header.index("Latitude")
        lonIndex = header.index("Longitude")
        lapIndex = header.index("Lap")
        timeIndex = header.index("Time")
        #Create dictionary to store lap information
        trackDict={}
        coordList=[]
        #Create dictionary to store time information
        timeDict = {}
        lapStartTime = 0
        lapFinishTime = 0
        for row in csvReader:
            lat = row[latIndex]
            lon = row[lonIndex]
            lap = row[lapIndex]
            time = row[timeIndex]
            #Skip over rows that do not have a lap number
            if not lap:
                continue
            #If current lap is in the dictionary, add the coordinates to the list
            elif lap in trackDict:
                coordList.append([lon, lat])
                trackDict[lap] = coordList
                #Set current time to lapFinishTime and subtract start time for total lap time so far.
                lapFinishTime = float(time)
                timeDict[lap] = lapFinishTime - lapStartTime
            #If current lap is not in the dictionary, reset coordinate list and start time.
            else:
                coordList=[]
                lapStartTime = float(time)
                coordList.append([lon, lat])
                trackDict[lap] = coordList  
        try:
            #Create polyline for each lap
            for lap in trackDict:
                CreatePolyline(lap)
                polylineFC = str(lap) + "Path.shp"
                coordList = trackDict[lap]
                lapTime = timeDict[lap]
                #Insert values for coordindates, lap number, and lap time
                with arcpy.da.InsertCursor(polylineFC, ("SHAPE@", "Lap", "Time")) as cursor:
                    cursor.insertRow((coordList, lap, lapTime))
                print("Successfully created polyline for " + str(lap))
        except: 
            print("Could not create polyline")
except:
    print("Could not read csv file successfully")
          
        
        
        
            
            
        
        
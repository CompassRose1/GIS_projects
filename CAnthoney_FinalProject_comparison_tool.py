# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 21:24:00 2021

@author: Cheryl
"""

import arcpy
import statistics

arcpy.env.workspace = "C:\\PSU\\Geog485"

#Get feature classes and field to compare
input1 = arcpy.GetParameterAsText(0)
input2 = arcpy.GetParameterAsText(1)
fieldName = arcpy.GetParameterAsText(2)

#Create field lists
fields1 = arcpy.ListFields(input1)
fields2 = arcpy.ListFields(input2) 

#Validate that field is numeric and exists in both feature classes

valid1 = False
valid2 = False

 
for field in fields1:
    #Check if field exists in feature class
    if field.name == fieldName:
        #Check if field type is numeric
        if field.type == "Short" or field.type == "Long" or field.type == "Single" or field.type == "Double":
            valid1 = True
        else:
            continue
    else:
        continue
    arcpy.AddMessage(arcpy.GetMessages())

for field in fields2:
    #Check if field exists in feature class
    if field.name == fieldName:
        #Check if field type is numeric
        if field.type == "Short" or field.type == "Long" or field.type == "Single" or field.type == "Double":
            valid2 = True
        else:
            continue
    else:
        continue
    arcpy.AddMessage(arcpy.GetMessages())

#Define function to report comparisons

def ReportComparison(stat, value1, value2):
    if value2 > value1:
        diff = value2-value1
        arcpy.AddMessage("The " + stat + " of " + fieldName + " for the first input is " + str(diff) + " lower than the second input.")
    elif value1 > value2: 
       diff = value1-value2 
       arcpy.AddMessage("The " + stat + " of " + fieldName + " for the first input is " + str(diff) + " higher than the second input.")
    else:
        arcpy.AddMessage("The " + stat + " of " + fieldName + " for the first input is the same as the second input.")
    
#Check if all conditions are met  
try:
    if valid1 == True and valid2 == True:
        #Read through the fields and calculate statistics for first input
        sum1 = 0
        total1 = 0
        firstValue1 = True
        numList1 = []
        with arcpy.da.SearchCursor(input1, (fieldName,)) as cursor:
            for row in cursor:
                sum1 += row[0]
                total1 += 1
                # Check if any values established yet 
                if firstValue1 == True:
                    min1 = row[0]
                    max1 = row[0]
                    firstValue1 = False
                    numList1.append(row[0])
                else:
                    numList1.append(row[0])
                    #If minimum and maximum already established, check for new min and max
                    if min1 > row[0]:
                        min1 = row[0]
                    if max1 < row[0]:
                        max1 = row[0]
                    else:
                        continue
                arcpy.AddMessage(arcpy.GetMessages())
        avg1 = sum1 / total1
        #Calculate standard deviation for the first input
        stdDev1 = statistics.stdev(numList1)
        sum2 = 0
        total2 = 0
        firstValue2 = True
        numList2 = []
        with arcpy.da.SearchCursor(input2, (fieldName,)) as cursor:
            for row in cursor:
                sum2 += row[0]
                total2 += 1
                # Check if any values established yet
                if firstValue2 == True:
                    min2 = row[0]
                    max2 = row[0]
                    firstValue2 = False
                    numList2.append(row[0])
                #If minimum and maximum already established, check for new min and max
                else:
                    numList2.append(row[0])
                    if min2 > row[0]:
                        min2 = row[0]
                    if max2 < row[0]:
                        max2 = row[0]
                    else:
                        continue
            arcpy.AddMessage(arcpy.GetMessages())
        avg2 = sum2 / total2
        stdDev2 = statistics.stdev(numList2)
        arcpy.AddMessage("The sum of " + fieldName + " for the first input is " +str(sum1) + " and for the second input is " +str(sum2))
        ReportComparison("sum", sum1, sum2)
        arcpy.AddMessage("The average of " + fieldName + " for the first input is " + str(avg1)+ " and the average for the second input is " +str(avg2))
        ReportComparison("average", avg1, avg2)
        arcpy.AddMessage("The minimum of "+ fieldName + " for the first input is " + str(min1) + " and the minimum for the second input is " + str(min2))
        ReportComparison("minimum", min1, min2)
        arcpy.AddMessage("The maximum of " + fieldName + " for the first input is " + str(max1) + " and the maximum for the second input is " + str(max2))
        ReportComparison("maximum", max1, max2)
        arcpy.AddMessage("The standard deviation of " + fieldName + " for the first input is " + str(stdDev1) + "and the standard deviation for the second input is " + str(stdDev2))
        ReportComparison("standard deviation", stdDev1, stdDev2)
    else:
        arcpy.AddError("Field not valid for both datasets")
except:
    arcpy.AddError("Unable to calculate statistics")


import arcpy, time, datetime
from arcpy.sa import *
from arcpy import env

ExecutionStartTime = datetime.datetime.now()
print 'Started: %s\n' % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')

env.workspace = r"R:\Divisions\Distribution\Shared\TechnicalScvs\ProjectFiles\EngProjects\Customer_Complaints\Density.gdb"
env.overwriteOutput = True


mxd = arcpy.mapping.MapDocument("R:/Divisions/Distribution/Shared/TechnicalScvs/ProjectFiles/EngProjects/Customer_Complaints/Density.mxd")
df  = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
for df in arcpy.mapping.ListDataFrames(mxd):
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, "DensityGroupLayer", df)[0]
    
    # Add Raster Layer to Density Group Layer
    for raster in arcpy.ListRasters("D*"):              # List all rasters that start with a 'D'
        rasterLayerName = raster+"_lyr"
        result          = arcpy.MakeRasterLayer_management(raster, rasterLayerName)
        layer           = result.getOutput(0)
        arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, layer, "AUTO_ARRANGE")

        arcpy.RefreshTOC()                              # REFRESH
        arcpy.RefreshActiveView()

        for target in targetGroupLayer:
            # Add Symbology to Raster Layer in Density Group Layer
            inputLayer      = target                    # Layer to apply symbology to
            sourceLayer     = "R:/Divisions/Distribution/Shared/TechnicalScvs/ProjectFiles/EngProjects/Customer_Complaints/Stretched_8STD.lyr"
            symbologyLayer  = arcpy.mapping.Layer(sourceLayer)
            #arcpy.ApplySymbologyFromLayer_management(inputLayer, symbologyLayer)
            arcpy.mapping.UpdateLayer(df, inputLayer, symbologyLayer, True)


            dataRange = raster[8:]
            m = dataRange[4:6]                          # Changes dynamic text in mxd to match new dataframe name 
            y1 = dataRange[0:4]                         # Example - 'From 12 1996 to 12 2001'
            y2 = dataRange[7:11]
            rasterName = "From " + m +" "+ y1 + " to " + m +" "+ y2

            df.name = rasterName                        # Change dataframe name to the date
            
            arcpy.RefreshTOC()                          # REFRESH
            arcpy.RefreshActiveView()

            # Export the map to a .jpg
            jpg = "R:/Divisions/Distribution/Shared/TechnicalScvs/ProjectFiles/EngProjects/Customer_Complaints/Density_JPGs/" + raster + ".jpg"
            arcpy.mapping.ExportToJPEG(mxd, jpg)
            print "Completed: " + raster

            df.name = "Layers"                          # Change dataframe name back to Layers
            
            # Remove Layer from Density Group Layer
            arcpy.mapping.RemoveLayer(df, target)

            arcpy.RefreshTOC()                          # REFRESH
            arcpy.RefreshActiveView()

del mxd


ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime

print 'Ended: %s\n' % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print 'Elapsed Time: %s' % str(ElapsedTime).split('.')[0]





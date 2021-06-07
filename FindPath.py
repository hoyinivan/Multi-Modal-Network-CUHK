import arcpy
from arcpy import env
env.workspace= "C:\MultimodalCUHK"
env.extent = "C:/MultimodalCUHK/Data/cuhk_map.tif" 
env.overwriteOutput = True
arcpy.CheckOutExtension("Network")

# Parameters
start_location = arcpy.GetParameterAsText(0) 
end_location = arcpy.GetParameterAsText(1) 
DayNight = arcpy.GetParameterAsText(2)
Walkingspeed = arcpy.GetParameterAsText(3)
BusPreference = arcpy.GetParameterAsText(4)

# Local variables:
CUHK_ND = "C:\\MultimodalCUHK\\Data\\CUHK.gdb\\Network\\CUHK_ND"
Route = "Route"
Route__5_ = "Route"
Route__3_ = "Route"
Route__2_ = "Route"
Routes = "Route\\Routes"
PathResult_shp = "C:\\MultimodalCUHK\\Result\\PathResult.shp"
outDirectionsFile = "C:/MultimodalCUHK/Result/Directions.txt"

# Get location
all_location = "Data\CUHK.gdb\Building\CUHK_Building_pt"
Start_point = "Result\Start_point.shp" 
arcpy.Select_analysis(all_location, Start_point, "\"Name_code\" = '"+start_location+"'")
End_point = "Result\End_point.shp" 
arcpy.Select_analysis(all_location, End_point, "\"Name_code\" = '"+end_location+"'")

# Choose impetus 
if BusPreference == "I want to walk only":
    if Walkingspeed == "Fast":
        Impetus = "Walk_Fast"
    elif Walkingspeed == "Normal":
        Impetus = "Walk_Normal"
    elif Walkingspeed == "Slow":
        Impetus = "Walk_Slow"
        
elif DayNight == "Day time":
    if Walkingspeed == "Fast":
        Impetus = "Daytime_Fast"
    elif Walkingspeed == "Normal":
        Impetus = "Daytime_Normal"
    elif Walkingspeed == "Slow":
        Impetus = "Daytime_Slow"
        
elif DayNight == "Night time":
    if Walkingspeed == "Fast":
        Impetus = "Nighttime_Fast"
    elif Walkingspeed == "Normal":
        Impetus = "Nighttime_Normal"
    elif Walkingspeed == "Slow":
        Impetus = "Nighttime_Slow"

# Choose hierarchy 
if BusPreference == "I like taking school bus":
    hierarchy_option = "USE_HIERARCHY"
else:
    hierarchy_option = "NO_HIERARCHY"

# Make Route Layer and Solve
arcpy.MakeRouteLayer_na(CUHK_ND, "Route", Impetus, "USE_INPUT_ORDER", "PRESERVE_BOTH", "NO_TIMEWINDOWS", "", "ALLOW_UTURNS", "", hierarchy_option, "", "TRUE_LINES_WITH_MEASURES", "")
arcpy.AddLocations_na(Route, "Stops", Start_point, "", "5000 Meters", "", "NightBus NONE;NightBus_Transfer NONE;SchoolBus NONE;SchoolBus_Transfer NONE;WalkingRoad SHAPE;CUHK_ND_Junctions NONE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "INCLUDE", "NightBus #;NightBus_Transfer #;SchoolBus #;SchoolBus_Transfer #;WalkingRoad #;CUHK_ND_Junctions #")
arcpy.AddLocations_na(Route__5_, "Stops", End_point, "", "5000 Meters", "", "NightBus NONE;NightBus_Transfer NONE;SchoolBus NONE;SchoolBus_Transfer NONE;WalkingRoad SHAPE;CUHK_ND_Junctions NONE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "INCLUDE", "NightBus #;NightBus_Transfer #;SchoolBus #;SchoolBus_Transfer #;WalkingRoad #;CUHK_ND_Junctions #")
arcpy.Solve_na(Route__3_, "SKIP", "TERMINATE", "")
arcpy.SelectData_management(Route__2_, "Routes")
arcpy.CopyFeatures_management(Routes, PathResult_shp, "", "0", "0", "0")
arcpy.Directions_na(Route__2_,"TEXT",outDirectionsFile,"Meters","REPORT_TIME",Impetus)

# Add the result to display
mxd = arcpy.mapping.MapDocument("CURRENT") 
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0] 
lyr = arcpy.mapping.Layer("Routes") 
arcpy.mapping.AddLayer(df,lyr)

# Show direction file
with open("C:/MultimodalCUHK/Result/Directions.txt", "r") as file:
  for line in file:
    arcpy.AddMessage(line)
arcpy.AddMessage("Direction File saved to C:/MultimodalCUHK/Result/Directions.txt")

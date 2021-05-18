import arcpy
from arcpy import mp
import os
from datetime import date

# get the date
today = date.today()
strDate = str(today.month).zfill(2) + str(today.day).zfill(2) +  str(today.year)

#: Global variables
networkdataset_path = "C:/Users/gbunce/Documents/projects/NetworkDataset/RecentBuilds/2021_5_6/UtahRoadsNetworkAnalysis.gdb/NetworkDataset/UtahRoadsNetwork"
input_stops = "C:/Users/gbunce/Documents/projects/network_analyst_distance_between_two_points/stops.gdb/testing_stops"
input_stops_routename_field = "RouteName" # this field will be used to create separate routes based on unique group id. it allows you to generate multiple routes in a single analysis. You can group stops into separate routes using their RouteName field values; one route is generated for each group.
output_layer_file = "C:/Users/gbunce/Documents/projects/network_analyst_distance_between_two_points/routes_lyr_" + strDate + ".lyrx" # this layer can only be viewed in Pro applications
output_route_fgdb = "C:/Users/gbunce/Documents/projects/network_analyst_distance_between_two_points/output_routes.gdb"

def main():
    try:
        #: Check out network analyst extension.
        if arcpy.CheckExtension("network") == "Available":
            arcpy.CheckOutExtension("network")
        else:
            raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

        # Create a network dataset layer.
        print("Make Route Layer")
        result_object = arcpy.na.MakeRouteAnalysisLayer(networkdataset_path, "Route", '', "USE_CURRENT_ORDER", None, "LOCAL_TIME_AT_LOCATIONS", "ALONG_NETWORK", None, "DIRECTIONS", "LOCAL_TIME_AT_LOCATIONS")

        #: Get the layer object from the result object. The Route layer can now be referenced using the layer object.
        layer_object = result_object.getOutput(0)

        #: Add Stops (these will be the locations in which the distance between them will be calculated)
        print("Add Route Locations")
        arcpy.na.AddLocations(layer_object, "Stops", input_stops, "Name # #;RouteName " + input_stops_routename_field + " #;Sequence # #;TimeWindowStart # #;TimeWindowEnd # #;LocationType # 0;CurbApproach # 0;Attr_TravelMinutes # 0;Attr_Length # 0", "5000 Meters", None, "'Roads : Limited Access & Ramps' SHAPE;'Roads : Other' SHAPE;UtahRoadsNetwork_Junctions NONE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "EXCLUDE", None)

        #: Solve the Route layer.
        print("Solve Route")
        arcpy.na.Solve(layer_object)

        #: Save the Route layer as a layer file on disk (however, the data in stored here: C:\Users\gbunce\AppData\Local\Temp\scratch.gdb)
        print("Save Route as Layer File")
        layer_object.saveACopy(output_layer_file)

        #: Export Route layers (from: C:\Users\gbunce\AppData\Local\Temp\scratch.gdb\Route\Routes) to fbdb feature classes
        # List sublayers in layer_object Group and export Routes and Stops
        print("Export Route layer to fgdb feature classes.")
        for lyr in layer_object.listLayers():
            if lyr.isGroupLayer:
                continue
            if str(lyr.name).startswith('Routes') or str(lyr.name).startswith('Stops'):
                arcpy.management.CopyFeatures(lyr, os.path.join(output_route_fgdb, lyr.name + strDate))

        #: Done
        print("Script completed successfully")

    except Exception as e:
        # If an error occurred, print line number and error message
        import traceback, sys
        tb = sys.exc_info()[2]
        print("An error occurred on line %i" % tb.tb_lineno)
        print(str(e))

#: Call the main function.
main()

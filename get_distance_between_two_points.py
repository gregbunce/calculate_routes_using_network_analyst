import arcpy
from arcpy import env
import os

#: Global variables
networkdataset_path = "C:/Users/gbunce/Documents/projects/NetworkDataset/RecentBuilds/2021_5_6/UtahRoadsNetworkAnalysis.gdb/NetworkDataset/UtahRoadsNetwork"
networkdataset_layer_name = "UtahRoadsNetwork"
input_stops = "C:/Users/gbunce/Documents/projects/network_analyst_distance_between_two_points/stops.gdb/testing_stops"
output_layer_file = "C:/Users/gbunce/Documents/projects/network_analyst_distance_between_two_points/testing_lyr.lyrx" # this layer can only be viewed in Pro applications

def main():
    try:
        #: Check out network analyst extension.
        if arcpy.CheckExtension("network") == "Available":
            arcpy.CheckOutExtension("network")
        else:
            raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

        # Create a network dataset layer. The layer will be referenced using its name.
        result_object = arcpy.na.MakeRouteAnalysisLayer(networkdataset_path, "Route", '', "USE_CURRENT_ORDER", None, "LOCAL_TIME_AT_LOCATIONS", "ALONG_NETWORK", None, "DIRECTIONS", "LOCAL_TIME_AT_LOCATIONS")

        #: Get the layer object from the result object. The route layer can now be referenced using the layer object.
        layer_object = result_object.getOutput(0)

        #: Add Stops (these will be the locations in which the distance between them will be calculated)
        arcpy.na.AddLocations(layer_object, "Stops", input_stops, "Name # #;RouteName RouteName #;Sequence # #;TimeWindowStart # #;TimeWindowEnd # #;LocationType # 0;CurbApproach # 0;Attr_TravelMinutes # 0;Attr_Length # 0", "5000 Meters", None, "'Roads : Limited Access & Ramps' SHAPE;'Roads : Other' SHAPE;UtahRoadsNetwork_Junctions NONE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "EXCLUDE", None)

        #: Solve the closest facility layer.
        arcpy.na.Solve(layer_object)

        #: Save the solved closest facility layer as a layer file on disk
        layer_object.saveACopy(output_layer_file)

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

#: resources:
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/network-analyst/solve.htm
# https://pro.arcgis.com/en/pro-app/latest/arcpy/network-analyst/performing-network-analysis.htm
# https://pro.arcgis.com/en/pro-app/latest/arcpy/network-analyst/route.htm
# https://pro.arcgis.com/en/pro-app/latest/help/analysis/networks/route-tutorial.htm
# https://pro.arcgis.com/en/pro-app/latest/help/analysis/networks/route-analysis-layer.htm




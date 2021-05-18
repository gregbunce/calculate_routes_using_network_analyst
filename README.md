The script in this repo creates routes between two or more points using an esri road centerline network dataset.  These routes are calculated using the [UGRC's](https://gis.utah.gov/) Statewide [Street Network Dataset](https://gis.utah.gov/data/transportation/street-network-analysis/#StreetNetwork), which is built from [UGRC's](https://gis.utah.gov/) statewide [Road Centerline](https://gis.utah.gov/data/transportation/roads-system/#RoadCenterlines) GIS layer.

This script requires an esri [network analyst](https://www.esri.com/en-us/arcgis/products/arcgis-network-analyst/overview) license.

It also requires an input table (feature class) of stop locations (beginning and end points). It is a recommended (but, not required) for that table to be in the following schema:

[Field Name] | [Data Type]
- Address | Text
- Shape | Point Geometry
- RouteName | Text *(You can group stops into separate routes using their [RouteName](https://pro.arcgis.com/en/pro-app/latest/help/analysis/networks/route-analysis-layer.htm) field values; one route is generated for each group)*

This script also requires an output file geodatabase where the calculated routes (and stops) will be exported.

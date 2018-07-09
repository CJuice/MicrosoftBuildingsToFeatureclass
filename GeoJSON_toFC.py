"""
Forked from @germrothdaniel on GitHub
Standalone python script to be run from an IDE. Built using ESRI ArcPro Python 3.6 version.
User needs to edit the variables that have an "EDIT VALUE" comment next to them. The script needs the path to an
ESRI geodatabase, a json file from the Microsoft Building Footprint Dataset, a name for the output feature class,
and the output WKID value used in projecting polygons for the users geographic location. Features are written to
the geodatabase feature class at an interval of every 10,000 polygons as a default. The user can edit this value
if they desire.
Date: 20180709
Author: CJuice
Revisions:
"""

def main():
    # IMPORTS
    import json
    import arcpy
    import os
    import time
    from collections import namedtuple

    Variable = namedtuple("Variable",["value"])

    # VARIABLES
        # constants
    INPUT_JSON_FILE_PATH = Variable(value=r"-9999")                         # EDIT VALUE
    INTERVAL = Variable(value=10000)                                        # OPTIONAL EDIT
    OUTPUT_FEATURE_CLASS_NAME = Variable(value="-9999")                     # EDIT VALUE
    OUTPUT_GEODATABASE_PATH = Variable(value=r"-9999")                      # EDIT VALUE
    SPATIAL_REFERENCE_INPUT = Variable(value=arcpy.SpatialReference(4326))
    SPATIAL_REFERENCE_OUTPUT_WKID = Variable(value=-9999)                   # EDIT VALUE

        # derived/other
    arcpy.env.overwriteOutput = True
    spatial_reference_object_output = arcpy.SpatialReference(SPATIAL_REFERENCE_OUTPUT_WKID.value)

    def polygon_generator(json_features):
        """
        Yield a projected polygon object from the loaded json file contents

        This is a generator function. Rather than loading all polygons at once and storing them in memory, per the
        previous scripting style, this function yields one polygon at a time.

        :param json_features: json features loaded/created from the Microsoft json file of interest
        :return: a polygon object, ready for insertion into the users feature class.
        """

        for feature in json_features:
            feature_xy_list = feature['geometry']['coordinates'][0]
            polygon_object = arcpy.Polygon(arcpy.Array([arcpy.Point(coordinates[0], coordinates[1]) for
                                                        coordinates in feature_xy_list]),
                                 SPATIAL_REFERENCE_INPUT.value)
            poly_out = polygon_object.projectAs(spatial_reference_object_output)
            yield poly_out

    def calculate_upper_range(num_features):
        """
        Determine the integer ceiling, by interval, for iteration

        :param num_features: The number of polygons of processing
        :return: upper range integer value
        """
        return ((num_features // INTERVAL.value) + 2)

    print("Script initiated at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.CreateFeatureclass_management(out_path=OUTPUT_GEODATABASE_PATH.value,
                                        out_name=OUTPUT_FEATURE_CLASS_NAME.value,
                                        spatial_reference=spatial_reference_object_output)
    print("Empty feature class created at {}".format(os.path.join(OUTPUT_GEODATABASE_PATH.value,
                                                                  OUTPUT_FEATURE_CLASS_NAME.value)))
    output_feature_class_full_path = os.path.join(OUTPUT_GEODATABASE_PATH.value, OUTPUT_FEATURE_CLASS_NAME.value)
    print("Loading json file...")
    with open(INPUT_JSON_FILE_PATH.value) as infile:
        json_raw_dataDict = json.load(infile)

    # Need dictionary of features from raw json data dictionary
    json_features = json_raw_dataDict['features']
    number_of_polygons = len(json_features)
    print("There are {:,} features to be processed into polygons".format(number_of_polygons))

    # Need projected polygons to write to feature class
    poly_gen = polygon_generator(json_features=json_features)
    print("Processing polygons...")

    # Need to write polygons to the feature class in user-defined quantities (INTERVAL.value).
    counter = 0
    upper_range = calculate_upper_range(num_features=number_of_polygons)
    for i in range(1,upper_range):
        with arcpy.da.InsertCursor(output_feature_class_full_path, 'SHAPE@') as insert_cursor:
            for poly in poly_gen:
                if counter == 0 or counter % INTERVAL.value != 0:
                    insert_cursor.insertRow([poly])
                    counter += 1
                else:
                    insert_cursor.insertRow([poly])
                    counter += 1
                    break
        print("{:,} of {:,} polygons written to {} {}".format((i*INTERVAL.value),
                                                              number_of_polygons,
                                                              OUTPUT_FEATURE_CLASS_NAME.value,
                                                              time.strftime("%H:%M:%S")))
    print("{:,} polygons were created.".format(counter))
    print("Script complete at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == "__main__":
    main()
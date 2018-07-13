# MicrosoftBuildingsToFeatureclass

Forked from @germrothdaniel on GitHub

Standalone python script to be run from an IDE. Built using ESRI ArcPro Python 3.6 version.

User needs to edit the variables that have an "EDIT VALUE" comment next to them. The script needs the path to an
ESRI geodatabase, a json file from the Microsoft Building Footprint Dataset, a name for the output feature class,
and the output WKID value used in projecting polygons for the users geographic location. Features are written to
the geodatabase feature class at an interval of every 10,000 polygons as a default. The user can edit this value
if they desire.

![Where to edit.](https://github.com/CJuice/MicrosoftBuildingsToFeatureclass/blob/master/WhereToEdit.PNG)
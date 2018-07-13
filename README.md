# MicrosoftBuildingsToFeatureclass

Forked from @germrothdaniel on GitHub

Standalone python script to be run from an IDE. Built with ESRI ArcPro Python 3.6 version as the interpreter.

User needs to edit the variables that have an "EDIT VALUE" comment next to them. These variables have a -9999 as a 
placeholder (see image below). 

The script needs the path to an ESRI geodatabase, a json file from the Microsoft Building Footprint 
Dataset, a name for the output feature class, and the output WKID value used in projecting polygons for the users
geographic location. Features are written to the geodatabase feature class at an interval of every 10,000 polygons
as a default. The user can edit this value if they desire.

![Where to edit the script.](https://github.com/CJuice/MicrosoftBuildingsToFeatureclass/blob/master/WhereToEdit.PNG)
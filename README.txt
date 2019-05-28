This is a stub project created by the ArcGIS Desktop Python AddIn Wizard.

Add-in is intended to create a user-generated polyline in ArcGIS Desktop 10.1+, 
then creates a supplemental image file showing the elevation profile along that route.
Profile Image is saved as external file, and can be inserted into a map document as needed.
Polyline route is retained as feature layer "Route" after process completes. User can 
specify units for horizontal measure, but units for elevation and vertical datum is 
entirely dependent on raster used for processing.  

Note: All functionality extends from Elevation_Profile_addin.py in Install directory.

INSTALLATION: For use with ArcGIS Desktop 10.1+ only. Double-click "makeaddin.py" file to create 
"Elevation_Profile.esriaddin" file in same root directory.  Double click this addin, and click button
"Install Add-In".  This should install Elevation_Profile as a toolbar in your ArcGIS installation, 
as indicated in your system registry.

Dependencies: matplotlib Python module used for creating actual profile graphs, and this is 
saved in Install directory (as required for creating a functioning, zipped add-in).  ArcGIS 
Desktop Spatial Analyst extension required for processing (an alert will notify you if this 
is not accessible).  

MANIFEST
========

README.txt   : This file

makeaddin.py : A script that will create a .esriaddin file out of this 
               project, suitable for sharing or deployment

config.xml   : The AddIn configuration file

Images/*     : all UI images for the project (icons, images for buttons, 
               etc)

Install/*    : The Python project used for the implementation of the
               AddIn. The specific python script to be used as the root
               module is specified in config.xml.


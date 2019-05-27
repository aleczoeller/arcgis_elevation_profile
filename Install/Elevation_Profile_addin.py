# -*- coding: utf-8 -*-

"""
***************************************************************************
    Elevation_Profile_addin.py
    ---------------------
    Date                 : May 2019
    Copyright            : (C) 2019 by Alec Zoeller
    Email                : alec zoeller at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 3 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__version__ = '0.1'
__author__ = 'Alec Zoeller'
__copyright__ = '(c) 2019 by Alec Zoeller'


import sys
import os
sys.path.append(os.path.dirname(__file__))

import arcpy
import pythonaddins

from matplotlib import pyplot as plt


class ComboBoxRaster(object):
    """Implementation for Elevation_Profile_addin.raster_layer_menu (ComboBox)"""
    def __init__(self):        
        #At initiation, pull all rasters from dataframe into drop-down list of rasters for analysis.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyrs = [i.name for i in arcpy.mapping.ListLayers(mxd) if i.isRasterLayer == True]
        del mxd
        self.items = lyrs
        if len(lyrs) > 0:
            self.raster_layer = lyrs[0]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
    def onSelChange(self, selection):
        self.raster_layer = selection
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass


class ComboBoxUnits(object):
    """Implementation for Elevation_Profile_addin.meas_units (ComboBox)"""
    def __init__(self):
        #Default units is feet
        self.items = ["Feet", "Yards", "Miles", "Meters", "Kilometers"]
        self.units = 'Feet'
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWW'
        self.width = 'WWWWWWWWWWW'
    def onSelChange(self, selection):
        self.units = selection
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ElevationProfiler(object):
    """Implementation for Elevation_Profile_addin.profile_tool (Tool)
    
    Primary tool functionality.  Create polyline, densify to add 400 evenly spaced
    additional segments, attribute elevation from specified raster and create
    and output an Elevation Profile graph.  
    """
    def __init__(self):
        self.enabled = True
        self.shape = "Line"
        self.cursor = 3
        self.point_list = []
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        if button == 3:
            self.point_list.append([x, y])
        else:
            pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        self.line_geometry = line_geometry
        try:
            arcpy.CheckOutExtension('SPATIAL')
        except Exception as e:
            arcpy.AddError('Spatial Extension required.\r\n' + str(e))
        raster_layer = raster_layer_menu.raster_layer
        poly = self.line_geometry
        use_units = meas_units.units
        poly_length = poly.getLength(units='{}'.format(use_units))
        dens_distance = int(poly_length/400)
        arcpy.env.overwriteOutput = True
        arcpy.CopyFeatures_management(poly, 'in_memory\\Route')
        arcpy.Densify_edit(r'in_memory\Route', 'DISTANCE', str(dens_distance) + ' {}'.format(use_units))
        arcpy.FeatureVerticesToPoints_management('in_memory\\Route', 'in_memory\\poly_feature', 'ALL')
        pts = [list(i[0]) for i in arcpy.da.SearchCursor('in_memory\\poly_feature', 'SHAPE@XY')]
        #Derive elevation values from DEM specified.  
        arcpy.sa.ExtractMultiValuesToPoints('in_memory\\poly_feature', [[raster_layer, 'Z']])
        arcpy.CheckInExtension('SPATIAL')
        elev = [i[0] for i in arcpy.da.SearchCursor('in_memory\\poly_feature', 'Z')]
        seg_length = int(poly_length/len(elev))
        splits = []
        for i in range(len(elev)):
            splits.append(i*seg_length)
        arcpy.Delete_management('poly_feature')
        #Produce and export elevation profile.
        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Elevation Profile')
        ax.plot(splits, elev, linewidth=2, color='g')
        fig.add_axes(ax)
        plt.xlabel('Feet Along Route')
        plt.ylabel('Elevation')
        try:
            plt.savefig(pythonaddins.SaveDialog('Save Elevation Profile', 'Profile.png',
                            os.path.dirname(arcpy.mapping.MapDocument("CURRENT").filePath)))
        except:
            pythonaddins.MessageBox('Error during save. Click reset and re-run process.', 'Alert')
    def onRectangle(self, rectangle_geometry):
        pass

class ResetButton(object):
    """Implementation for Elevation_Profile_addin.reset (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        meas_units.units = 'Feet'
        mxd = arcpy.mapping.MapDocument('CURRENT')
        lyrs = [i.name for i in arcpy.mapping.ListLayers(mxd) if i.isRasterLayer == True]
        if len(lyrs) > 0:
            raster_layer_menu.items = lyrs
            raster_layer_menu.raster_layer = lyrs[0]
        del mxd

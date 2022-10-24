# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flintpro_datackeckDialog
                                 A QGIS plugin
 Data input check for FLINTpro
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-09-15
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Harrison McKenzie-McHarg
        email                : harrison.mcharg@mulliongroup.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os, random, qgis, itertools, time, math

from itertools import combinations
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis import *
from math import comb
from qgis.gui import *
from qgis import processing
from qgis.utils import iface


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'flintpro_datacheck_dialog_base.ui'))

reqcheck = 3

class flintpro_datackeckDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(flintpro_datackeckDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.PB_Check_Button.clicked.connect(self.requirement_check)
        self.PB_Check_Button.clicked.connect(self.reset)
        self.button_box.clicked.connect(self.reset)
        self.button_box.clicked.connect(self.resettodefault)
        self.PB_Check_Button.clicked.connect(self.isspatial)
        self.PB_Check_Button.clicked.connect(self.storagetype)
        self.PB_Check_Button.clicked.connect(self.attributes)
        self.PB_Check_Button.clicked.connect(self.geometrytype)
        self.PB_Check_Button.clicked.connect(self.projection)
        self.PB_Check_Button.clicked.connect(self.overlapcheck)
        self.PB_Check_Button.clicked.connect(self.check_validity)
        self.progressBar.setValue(0)
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed )
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.CB_upload_type.currentIndexChanged.connect(self.upload_type)  
        self.layout().addWidget(self.bar,0,0,0,0,QtCore.Qt.AlignTop)
    
    # creates a global variable so that the processes only run when correct options are selected in the dropdown boxes
    def requirement_check(self):
        global reqcheck
        layername = self.CB_maplayer.currentLayer()
        if self.CB_maplayer.currentLayer() is None:
            self.bar.pushMessage("No Input Layer Selected","Choose a layer that you would like to check from the dropdown menu.", level=qgis.core.Qgis.Info)
            reqcheck = 1
        else:
            reqcheck = 0
            
        if reqcheck is 0:
            if self.CB_upload_type.currentIndex() is 0:
                self.bar.pushMessage("No Upload Type Selected","Choose a data upload type from the dropdown menu", level=qgis.core.Qgis.Info)
                reqcheck = 1
        if reqcheck is 0:
            if self.CB_layer_class.currentIndex() is 0:
                self.bar.pushMessage("No Data Layer Classification Selected","Choose a data layer classification from the dropdown menu", level=qgis.core.Qgis.Info)
                reqcheck = 1
        if reqcheck is 0:
            if layername.type() not in ["QgsMapLayerType.VectorLayer"]:
                reqcheck = 1
                self.bar.pushMessage("Function not yet available","FLINTpro Datacheck for rasters is coming soon!", level=qgis.core.Qgis.Info)

                
    # warning message when Raster is selected as the data layer type
    def upload_type(self):
        global reqcheck
        if self.CB_upload_type.currentIndex() is 2:
                self.bar.pushMessage("Function not yet available","FLINTpro Datacheck for rasters is coming soon!", level=qgis.core.Qgis.Info)
                reqcheck = 1

    # resets all the outputs to blank
    def reset(self):
        self.Label_Errors.clear()
        self.Label_Format.clear()
        self.Label_Storage.clear()
        self.Label_Attributes.clear()
        self.Label_Geometry.clear()
        self.Label_Projection.clear()
        self.Label_Overlaps.clear()
        self.progressBar.setValue(0)
        
    # sets all inputs to default when the plugin is closed
    def resettodefault(self):
        self.CB_maplayer.setLayer(self.CB_maplayer.layer(0))
        self.CB_upload_type.setCurrentIndex(0)
        self.CB_layer_class.setCurrentIndex(0)

    # checks the layer is spatial using the isSpatial operation for vectors
    def isspatial(self):
        global reqcheck
        if reqcheck is 0:
            time.sleep(0.1)
            self.progressBar.setValue(5)
            layername = self.CB_maplayer.currentLayer()
            fields = layername.fields()
            if str(layername.isSpatial()) in ['True']:
                self.Label_Format.setText(u'\u2705'+'       Layer is spatial')
            else:
                self.Label_Format.setText(u'\u274C'+"        Layer is not in a spatial format") 
    
    # checks that the layer is GeoJSON            
    def storagetype(self):
        global reqcheck
        if reqcheck is 0:
            time.sleep(0.1)
            self.progressBar.setValue(10)
            layername = self.CB_maplayer.currentLayer()
            fields = layername.fields()
            time.sleep(0.1)
            if "GeoJSON" in layername.storageType():
                self.Label_Storage.setText(u'\u2705'+'       Correct format')
            else:
                self.Label_Storage.setText(u'\u274C'+"       Convert to GeoJSON")
    
    # checks that there is at least one attribute field that contains string type and is less than 50 chars
    def attributes(self):
        global reqcheck
        if reqcheck is 0:
            layername = self.CB_maplayer.currentLayer()
            fields = layername.fields()
            time.sleep(0.1)
            self.progressBar.setValue(15)
            for field in fields:
              if str(field.typeName()) in ['String'] and field.length()<50:
                self.Label_Attributes.setText(u'\u2705'+'       Appropriate attributes')
                break
              else:
                    self.Label_Attributes.setText(u'\u274C'+"       Layer must contain at least 1 'string' attribute")
    
    # checks that the data is multipolygon or polygon type. This also ensures there is no Z parameter.
    def geometrytype(self):
        global reqcheck
        if reqcheck is 0:
            layername = self.CB_maplayer.currentLayer()
            fields = layername.fields()
            time.sleep(0.1)
            self.progressBar.setValue(20)
            if str(layername.wkbType()) in ['3', '6']:
                self.Label_Geometry.setText(u'\u2705'+'       Correct geometry')
            else:
                self.Label_Geometry.setText(u'\u274C'+"       Convert geometry to Multipolygon")
    
    #checks that the projection is WGS84
    def projection(self):
        global reqcheck
        if reqcheck is 0:
            layername = self.CB_maplayer.currentLayer()
            fields = layername.fields()
            time.sleep(0.1)
            self.progressBar.setValue(25)
            if 'EPSG:4326' in str(layername.sourceCrs()):
                self.Label_Projection.setText(u'\u2705'+'       Correct projection')
            else:
                self.Label_Projection.setText(u'\u274C'+"       Reproject to WGS84 EPSG:4326")
    
    # checks for overlaps by measuring intersection of every combination of two features. zooms to the first overlap found and stops
    def overlapcheck(self):
        global reqcheck
        if reqcheck is 0:
            layername = self.CB_maplayer.currentLayer()
            fields = layername.fields()
            featnum = layername.featureCount()
            featurelist = [feature.id() for feature in layername.getFeatures()]
            time.sleep(0.1)
            self.progressBar.setValue(30)
            Overlaps = qgis.core.QgsGeometry.overlaps
            Geom = qgis.core.QgsGeometry
            get = layername.getGeometry
            combs = combinations(featurelist, 2) #for iterating through all combinations of values 0-n (inclusive) where n is the number of features
            n_combs = comb(featnum,2) #count of total combinations for updating progress bar
            index = 30 #for iterating progress bar value
            for com in combs:
                index += (20/n_combs)
                self.progressBar.setValue(int(index))
                pair = com
                x, y = pair
                if Geom.intersection(get(x),get(y)).area() > 0.0:
                    self.Label_Overlaps.setText(u"\u274C"+"        Features "+str(x)+" and "+str(y)+" have overlapping geometry")
                    layername.selectByIds([x,y])
                    box = layername.boundingBoxOfSelected()
                    iface.mapCanvas().setExtent(box)
                    iface.mapCanvas().refresh()
                    break
                else:
                    self.Label_Overlaps.setText(u'\u2705'+"       No overlaps found")
    
    # runs validity check for layer and returns number of errors found            
    def check_validity(self, parameters):
        global reqcheck
        if reqcheck is 0:
            layername = self.CB_maplayer.currentLayer()
            time.sleep(0.1)
            self.progressBar.setValue(60)
            if self.CB_upload_type.currentIndex() is 1:
                if self.CB_layer_class.currentIndex() in [1, 2, 3, 4]:
                    error_count=processing.run("qgis:checkvalidity",{'INPUT_LAYER':layername, 'ERROR_COUNT':'TEMPORARY_OUTPUT'})['ERROR_COUNT']
                    if error_count in [0]: 
                        self.Label_Errors.setText(u'\u2705'+'       '+str(error_count)+' errors found')
                    else:
                        self.Label_Errors.setText(u'\u274C'+'       '+str(error_count)+' errors found')
            time.sleep(0.1)
            self.progressBar.setValue(100)
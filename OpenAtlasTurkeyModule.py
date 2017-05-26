# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenAtlasTurkey
                                 A QGIS plugin
 OpenAtlasTurkey plugin provides collection of publicly available geospatial datasets for Turkey.
                              -------------------
        begin                : 2017-05-09
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Dr. Cem GULLUOGLU
        email                : cemgulluoglu@gmail.com
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
#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon,QTableWidgetItem,QMessageBox,QHeaderView,QFont,QWidget,QTextCursor, QPushButton, QFileDialog
#from PyQt4.QtGui import QGraphicsScene,QPixmap,QGraphicsPixmapItem,QPainter, QAbstractItemView

import sys
import os 

reload(sys)
sys.setdefaultencoding('utf-8')

#from PyQt4 import QtGui, QtCore

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from OpenAtlasTurkeyModule_dialog import OpenAtlasTurkeyDialog
from about_dialog import AboutDialog
import os.path

from qgis.gui import *
from qgis.core import *

import os.path, webbrowser,urllib,urlparse
import csv 

import urllib2, re

from PyQt4.QtCore import * #QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import * #QAction, QIcon
from qgis.core import *

global webServicesList

class OpenAtlasTurkey:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'OpenAtlasTurkey_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
        
        # Create the dialog (after translation) and keep reference
        self.dlg = OpenAtlasTurkeyDialog()
        self.dlgabout = AboutDialog()

        self.CSVpath = os.path.join(os.path.dirname(__file__),"data_sources.csv")
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Open Atlas Turkey')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'OpenAtlasTurkey')
        self.toolbar.setObjectName(u'OpenAtlasTurkey')
        

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('OpenAtlasTurkey', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = OpenAtlasTurkeyDialog()

        icon = QIcon(icon_path)
        
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/OpenAtlasTurkey/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Open Atlas Turkey'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Open Atlas Turkey'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

            
       

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

    # def LoadDatasets():
        
        #define CSV service sources file path
        f = open(self.CSVpath, "rb")
        #f = open ("C:\\Users\\%USERNAME%\\.qgis2\\python\\plugins\\OpenAtlasTurkey\\data_sources.csv", "rb")
        
        reader = csv.reader(f, delimiter=";",quoting=csv.QUOTE_NONE)   
        
        global webServicesList
        webServicesList = []

        for row in reader:
            webServicesList.append(row)
        
        #webServicesListMsg = u"Total_number_of_readed_rows_from_csv:"+str(len(webServicesList))
        #QMessageBox.warning(None,"Warning",webServicesListMsg)
                
        f.close() #close CSV file.
    
    
    #def FillTable():
        #global webServicesList
        #how many lines e.g. 59 incl. header
        #len(webServicesList)
        
        #define table col.          
        self.dlg.tableWidget.setRowCount(0)
        self.dlg.tableWidget.setColumnCount(6)

        #define table col. width  
        self.dlg.tableWidget.setColumnWidth(0,150)
        self.dlg.tableWidget.setColumnWidth(1,200)
        self.dlg.tableWidget.setColumnWidth(2,50)
        self.dlg.tableWidget.setColumnWidth(3,400)
        self.dlg.tableWidget.setColumnWidth(4,400)
        self.dlg.tableWidget.setColumnWidth(5,50)
        
        #define table col. width  
        self.dlg.tableWidget.setHorizontalHeaderLabels([u"Adı / Name", u"Veri Sahibi / Data Owner",u"OGC",u"Katman Bilgisi / Layer Information",u"Servis Adresi / Service URL", u"EPSG"])
        
        # qtableWidget behavour
        self.dlg.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dlg.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        #insert and list each service on table
        counter_j = 0
        while counter_j+1 < int(len(webServicesList)):
            self.dlg.tableWidget.insertRow(counter_j)
            counter_j = counter_j + 1
        
        counter_i = 1
        while counter_i < int(len(webServicesList)):
            #add table info
            self.dlg.tableWidget.setItem(counter_i-1 , 0, QTableWidgetItem(unicode(str(webServicesList[counter_i][0]),'utf-8'))) #servisAdi = row[0] from csv ;
            self.dlg.tableWidget.setItem(counter_i-1 , 1, QTableWidgetItem(unicode(str(webServicesList[counter_i][1]),'utf-8'))) #veriSahibi = row[1] from csv ;
            self.dlg.tableWidget.setItem(counter_i-1 , 2, QTableWidgetItem(unicode(str(webServicesList[counter_i][3]),'utf-8'))) #servisTipi = row[3] from csv ;
            self.dlg.tableWidget.setItem(counter_i-1 , 3, QTableWidgetItem(unicode(str(webServicesList[counter_i][6]),'utf-8'))) #ozetBilgi = row[6] from csv ;
            self.dlg.tableWidget.setItem(counter_i-1 , 4, QTableWidgetItem(unicode(str(webServicesList[counter_i][11]),'utf-8'))) #servisUrl = row[11] from csv ;
            self.dlg.tableWidget.setItem(counter_i-1 , 5, QTableWidgetItem(unicode(str(webServicesList[counter_i][13])[-4:],'utf-8'))) #temelKRS = row[13] from csv ;
            counter_i = counter_i + 1
            
            #servisSahibi = row[2]
            #servisVersiyonu = row[4]
            #servisYayimlanmaTarihi = row[5]           
            #anahtarKelimeler = row[7]
            #ilgiliKisi = row[8]
            #ilgiliKisiTel = row[9]
            #ilgiliKisiEposta = row[10]
            #metaveri = row[12]
            #sunucuTipi = row[14]
            #sunucuVersiyonu = row[15]
            #yetkiSeviyesi = row[16]
            #hukuki = row[17]
                
        
        def LoadLayerFunc():
            
            # get the selected row (list with indices)
            selectedIndexes = self.dlg.tableWidget.selectionModel().selectedRows()        
            row = selectedIndexes[0].row() #return table index 0 1 2 etc.
            
            # get name and service typeof selected row
            OGC_service_address = self.dlg.tableWidget.item(row, 4).text() # e.g. https://tucbs-public-api.csb.gov.tr/trk_hgk_idari_sinir_wms
            OGC_service_type = self.dlg.tableWidget.item(row, 2).text() #e.g. WMS 
            OGC_service_info = self.dlg.tableWidget.item(row, 3).text() #e.g. this service contains etc. 
            OGC_EPSG_code = self.dlg.tableWidget.item(row, 5).text()  #get epsg code
            OGC_EPSG_code_trim = str(OGC_EPSG_code)[-4:] #e.g. trim EPSG chars. to get 4326

            #QMessageBox.warning(None,"Warning","OGC_service_address:"+str(OGC_service_address))
            #QMessageBox.warning(None,"Warning","OGC_service_type:"+str(OGC_service_type))
            #QMessageBox.warning(None,"Warning","OGC_EPSG_code_:"+str(OGC_EPSG_code))

            global webServicesList
            tableindexno=str(webServicesList[3][11])
            webServicesListMsg = "clicked_table_index_no"+str(tableindexno)
            #QMessageBox.warning(None,"Warning",webServicesListMsg)

        
            #FOR WMS
            if str(OGC_service_type) == "WMS" or str(OGC_service_type) == "wms":
                
                file = urllib2.urlopen(str(OGC_service_address)+"?request=GetCapabilities&service=WMS&version1.3.0")
                #https://tucbs-public-api.csb.gov.tr/csb_cdp_abi_wms
                data = file.read()
                                
                #string = '<Name>(.+?)</Name>'
                string = u'<Layer.*?>\s*<\S*?Name>([^<]+)</\S*?Name>'
                
                layer = re.findall(string, data)
                NumberOfWMSLayers = str(len(layer))
                QMessageBox.information(None,"Bilgi / Information",NumberOfWMSLayers+" katman haritaya eklenecektir.\n"+NumberOfWMSLayers+" layer(s) will be added into map.")
                #QMessageBox.warning(None,"Warning","lyr:"+str(layer))
                
                for layer in layer:
                    if layer is not None:
                        #QMessageBox.warning(None,"Warning","if_layer_is_not_none:"+str(layer))
                        
                        #contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=1&styles=&url=https://tucbs-public-api.csb.gov.tr/csb_cdp_abi_wms
                        urlWithParams1 = 'url='+str(OGC_service_address)+'&format=image/png&layers='
                        urlWithParams2 = '&styles=&crs=EPSG:'+str(OGC_EPSG_code_trim)
                        
                        urlWithParams = urlWithParams1 + str(layer) + urlWithParams2
                        #urlWithParams = urlWithParams1 + str(j) + urlWithParams2
                        
                        #QMessageBox.warning(None,"Warning","URL_is:"+str(urlWithParams))
                        
                        wms_layer = "'"+str(layer)+"'"
                        #wms_layer = "'"+str(j)+"'"
                        
                        rlayer = QgsRasterLayer(urlWithParams, wms_layer , "wms") #wms must be in small letters (NOT "WMS")
                        #QgsMapLayerRegistry.instance().addMapLayer(rlayer)

                        root = QgsProject.instance().layerTreeRoot()  
                        LayerGroup = (unicode(str(OGC_service_type+" : "+OGC_service_info)))           

                        if root.findGroup(LayerGroup) not in root.children(): #add layer group into TOC once                         
                            self.iface.legendInterface().addGroup(LayerGroup) 
                        
                        #root = QgsProject.instance().layerTreeRoot()                        
                        mygroup = root.findGroup(LayerGroup)                        
                        parentGroup = mygroup.parent()                        
                        groupIndex=-1                        
                        for child in parentGroup.children():
                            groupIndex+=1
                            if mygroup == child:
                                break
                                
                        QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
                        mygroup.insertChildNode(groupIndex, QgsLayerTreeLayer(rlayer))
                        
                file.close()


            #FOR WFS
            elif str(OGC_service_type) == "WFS" or str(OGC_service_type) == "wfs":   
                #QMessageBox.warning(None,"Warning",OGC_service_address)
                file = urllib2.urlopen(str(OGC_service_address)+"?service=wfs&version=1.0.0&request=GetCapabilities")
                data = file.read()
                string = u'<\S*FeatureType><\S*Name>(.+?)</\S*Name><\S*Title>'
                
                for word in data.split():
                    layer = re.search(string, word)
                    NumberOfWFSLayers = str(len(re.findall(string, data)))
                    if layer is not None:
                        QMessageBox.information(None,"Bilgi / Information",NumberOfWFSLayers+" katman haritaya eklenecektir.\n"+NumberOfWFSLayers+" layer(s) will be added into map.")
                        #QMessageBox.warning(None,"Warning",str(layer))

                        uri = str(OGC_service_address)+"?srsname=EPSG:"+str(OGC_EPSG_code_trim)+"&typename={name}&version=1.0.0&request=vlayer=QgsVectorLayer".format(name = layer.group(1))
                        #QMessageBox.warning(None,"Warning","uri:"+str(uri))
                        vlayer = QgsVectorLayer(uri, layer.group(1), "WFS") #WFS must be in CAPITAL LETTERS (not "wfs")
                        #QgsMapLayerRegistry.instance().addMapLayer(vlayer)

                        root = QgsProject.instance().layerTreeRoot()  
                        LayerGroup = (unicode(str(OGC_service_type+" : "+OGC_service_info)))           

                        if root.findGroup(LayerGroup) not in root.children(): #add layer group into TOC once                         
                            self.iface.legendInterface().addGroup(LayerGroup) 
                        
                        #root = QgsProject.instance().layerTreeRoot()                        
                        mygroup = root.findGroup(LayerGroup)                        
                        parentGroup = mygroup.parent()                        
                        groupIndex=-1                        
                        for child in parentGroup.children():
                            groupIndex+=1
                            if mygroup == child:
                                break
                                
                        QgsMapLayerRegistry.instance().addMapLayer(vlayer, False)
                        mygroup.insertChildNode(groupIndex, QgsLayerTreeLayer(vlayer))
                        
                file.close()

            else:
                pass
                
        def Show_About():
            #self.dlgabout.exec_()
            self.dlgabout.show() 
            
        def CloseFunction():
            self.dlg.close()

        def AboutCloseFunction():
            self.dlgabout.close()              
  
        self.dlg.LoadLayer.clicked.connect(LoadLayerFunc)
        self.dlg.AboutButton.clicked.connect(Show_About)   
        self.dlg.CloseButton.clicked.connect(CloseFunction) 
        self.dlgabout.AboutCloseButton.clicked.connect(AboutCloseFunction) 


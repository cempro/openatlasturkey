# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenAtlasTurkeyDialog
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'OpenAtlasTurkeyModule_dialog_base.ui'))


class OpenAtlasTurkeyDialog(QtGui.QDialog, FORM_CLASS):

    closingPlugin = pyqtSignal()
    
    def __init__(self, parent=None):
        """Constructor."""
        super(OpenAtlasTurkeyDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

        

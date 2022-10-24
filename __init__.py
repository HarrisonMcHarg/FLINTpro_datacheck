# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flintpro_datackeck
                                 A QGIS plugin
 Data input check for FLINTpro
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-09-15
        copyright            : (C) 2022 by Harrison McKenzie-McHarg
        email                : harrison.mcharg@mulliongroup.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load flintpro_datackeck class from file flintpro_datackeck.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .flintpro_datacheck import flintpro_datackeck
    return flintpro_datackeck(iface)
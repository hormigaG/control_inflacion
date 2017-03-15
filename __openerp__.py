# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Control de inflacion',
    'version': '0.1',
    'category': 'sales',
    'description': """
Control de inflacion
======================
Permite la modificacion de manera bulk de el precio de costo de un producto
    """,
    'author': 'Filoquin',
    'website': 'http://sipecu.com.ar',
    'depends': ['base'],
    'installable': True,
    'data': ['control_inflacion.xml'],
    'images':[],    
    'auto_install': False,
}

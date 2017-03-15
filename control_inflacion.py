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

from datetime import datetime , timedelta ,  date 
from dateutil import parser

from openerp import models, fields, api ,  SUPERUSER_ID
from openerp import tools


from openerp.tools.translate import _
import re
import logging

import requests
from lxml import etree

_logger = logging.getLogger(__name__) 




class control_inflacion(models.Model):

    _name = 'control.inflacion'
    _description = 'Control de inflacion'


    name = fields.datetime('Fecha')
    user_id = fields.One2many('res.user')

    category_ids = fields.Many2many('product.category','saved_pricelist_products_rel','list_id','product_id','Categorias')
    supplier_ids = fields.Many2many('res.partner','saved_pricelist_supplier_rel','list_id','suplier_id','Vendedor')
    has_stock = fields.Boolean('Solo con stock')
    percent = fields.Float('%')

    state = fields.Selection('Estado',[('draft','Borrador'),('cancel','Cancelado'),('done','Realizado')])
    
    @api.one
    def cancelar(self):
        self['state']='cancel'

    @api.one
    def realizar(self):

        ids=[]
        categorys = []
        args = []
        if self.category_ids : 

            for parent_id in self.category_ids:
                childs = self.env['product.category'].search([('id','child_of',parent_id.id)])

                for child in childs:
                    categorys.append(child.id)

            args.append(('categ_id','in',categorys))

        if self.supplier_ids:
            supplier_ids = [x.id for x in self.supplier_ids] 
            args.append(('seller_ids.name','in',supplier_ids))

        if self.has_stock :
            args.append(('qty_available','>',1)) 

        coeff = 1 + (self.percent/100)
        products_tmpls = self.env['product.template'].search_read(args, ['standard_price'])        
        for product in products_tmpls:
            self.env['product.template'].write(product['id'] ,['standard_price':product['standard_price']*coeff])



        self['state']='done'



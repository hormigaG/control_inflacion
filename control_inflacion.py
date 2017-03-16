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


    state = fields.Selection([('draft','Borrador'),('cancel','Cancelado'),('done','Realizado')],default='draft')

    name = fields.Datetime('Fecha', default=datetime.now())
    user_id = fields.Many2one('res.users')

    category_ids = fields.Many2many('product.category','saved_pricelist_products_rel','list_id','product_id','Categorias')
    supplier_ids = fields.Many2many('res.partner','saved_pricelist_supplier_rel','list_id','suplier_id','Vendedor')
    has_stock = fields.Boolean('Solo con stock')
    percent = fields.Float()

    control_inflacion_items_ids = fields.One2many('control.inflacion.items','control_inflacion_id')



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
        products_tmpls = self.env['product.template'].search(args)        
        alter_items=[]
        for product in products_tmpls:
            product.write({'standard_price':product['standard_price']*coeff})
            alter_items.append(0,0,{'products_tmpl_id':product['id'],'old_value':product['standard_price'] , 'new_value':product['standard_price']*coeff})

        if alter_items:
            self['control_inflacion_items_ids']=alter_items    
        self['state']='done'


class control_inflacion_items(models.Model):

    _name = 'control.inflacion.items'
    _description = 'Control de inflacion'

    control_inflacion_id= fields.Many2one('control.inflacion')
    products_tmpl_id= fields.Many2one('product.template')
    old_value = fields.Float()
    new_value = fields.Float()

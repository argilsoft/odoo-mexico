# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: Luis Torres (luis_t@vauxoo.com)
############################################################################
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
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import pooler, tools


class stock_picking(osv.Model):
    _inherit = 'stock.picking'
    
    
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        if context is None:
            context = {}
        res = super(stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context=context)
        if inv_type in ('out_invoice', 'out_refund'):
            acc_payment_id = move.picking_id and move.picking_id.sale_id and \
                             move.picking_id.sale_id.acc_payment and \
                             move.picking_id.sale_id.acc_payment.id or False
            
            payment_method_id = move.picking_id and move.picking_id.sale_id and \
                             move.picking_id.sale_id.pay_method_id and \
                             move.picking_id.sale_id.pay_method_id.id or False            
        else:
            acc_payment_id = move.purchase_line_id and move.purchase_line_id.order_id and \
                             move.purchase_line_id.order_id.acc_payment and \
                             move.purchase_line_id.order_id.acc_payment.id or False
            
            payment_method_id = move.purchase_line_id and move.purchase_line_id.order_id and \
                             move.purchase_line_id.order_id.pay_method_id and \
                             move.purchase_line_id.order_id.pay_method_id.id or False
                    
        res.update({'acc_payment': acc_payment_id})
        res.update({'pay_method_id': payment_method_id})
        
        return res
        
        

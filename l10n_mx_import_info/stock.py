# -*- encoding: utf-8 -*-
# Author=Nhomar Hernandez nhomar@vauxoo.com
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import pooler, tools
from openerp import release


class stock_quant_package(osv.Model):
    _inherit = "stock.quant.package"
    _columns = {
        'import_id': fields.many2one('import.info', 'Pedimento Aduanal', required=False,
            help="Imformación de Importación (Pedimento aduanal), necesaria para Facturación Electrónica."),
    }

    
class stock_move(osv.osv):
    _inherit = "stock.move"    
    
    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type, context=None):
        
        res = super(stock_move, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context=context)
        tracking_ids = []
        invoice_line_custom_obj = self.pool.get('account.invoice.line.customs')
        for link in move.linked_move_operation_ids:
            if link.operation_id and link.operation_id.package_id and link.operation_id.package_id.import_id:
                tracking_ids.append(link.operation_id.package_id.import_id.id)
        if tracking_ids:
            res.update({'import_ids': [(6,0,tracking_ids)]})
        return res


#class sale_order_line(osv.Model):
#    _inherit = "sale.order.line"
    
#    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
    """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
    """
#        stock_move_obj = self.pool.get('stock.move')
#        invoice_line_custom_obj = self.pool.get('account.invoice.line.customs')
#        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id, context)
#        for procur in line.procurement_ids:
#            if line.product_id.track_all or (line.product_id.track_incoming and line.product_id.track_outgoing):
#                for move in procur.move_ids:
#                    for link in move.linked_move_operation_ids:
#                        if link.operation_id and link.operation_id.package_id and link.operation_id.package_id.import_id:
#                            x = invoice_line_custom_obj.create(cr, uid, {'account_invoice_line_id':line.id, 'import_id':link.operation_id.package_id.import_id.id})
#        return res    
    


# -*- encoding: utf-8 -*-
##############################################################################
# Copyright (c) 2011 OpenERP Venezuela (http://openerp.com.ve)
# All Rights Reserved.
# Programmed by: Israel Fermín Montilla  <israel@openerp.com.ve>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
from openerp import pooler
import datetime
import time

import math

class inherit_picking(osv.Model):
    
    '''Inherit sotck.picking to add the new payment term field sent from previous orders'''
    
    _inherit = 'stock.picking'
    

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        if context is None:
            context = {}
        res = super(inherit_picking,self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context=None)
        
        if inv_type in ('out_invoice', 'out_refund'):
            res.update({
                'pay_method_ids': move.picking_id.sale_id and \
                                    move.picking_id.sale_id.pay_method_id and \
                                    [(6, 0, [move.picking_id.sale_id.pay_method_id.id])] or False,
                'acc_payment': move.picking_id.sale_id and \
                                    move.picking_id.sale_id.acc_payment and \
                                    move.picking_id.sale_id.acc_payment.id or False,
                    })
        return res 


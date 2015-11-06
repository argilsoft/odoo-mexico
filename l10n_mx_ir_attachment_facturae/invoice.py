#!/usr/bin/python
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Vauxoo (<http://vauxoo.com>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Juan Carlos Funes(juan@vauxoo.com)
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import pooler, tools
from openerp import netsvc
import time
from openerp.exceptions import except_orm, Warning, RedirectWarning

class account_invoice(osv.Model):
    _inherit = 'account.invoice'

    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        ir_attach_facturae_mx_obj = self.pool.get('ir.attachment.facturae.mx')
        inv_type_facturae = {
            'out_invoice': True,
            'out_refund': True,
            'in_invoice': False,
            'in_refund': False}
        for inv in self.browse(cr, uid, ids, context=context):
            if inv_type_facturae.get(inv.type, False):
                ir_attach_facturae_mx_ids = ir_attach_facturae_mx_obj.search(
                    cr, uid, [('invoice_id', '=', inv.id)], context=context)
                for attach in ir_attach_facturae_mx_obj.browse(cr, uid, ir_attach_facturae_mx_ids, context=context):
                    if attach.state <> 'cancel':
                        ir_attach_facturae_mx_obj.signal_cancel(cr, uid, [attach.id], context=context)
        res = super(account_invoice, self).action_cancel(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S')})
        return res

    
    def check_partner_data(self, cr, uid, partner, context=None):
        if context is None:
            context = {}
    
        if not partner.is_company:
            raise except_orm(_('Advertencia'),_("Partner - (ID: %s) %s - has unckecked field 'Is Company', to use this partner in Invoices you must check this field") % (partner.id,partner.name))
        if not (partner.street and partner.city and partner.street2 and \
                partner.state_id and partner.zip and partner.l10n_mx_city2 and partner.country_id):
            raise except_orm(_('Advertencia'),_("Partner - (ID: %s) %s - has incomplete address, please verify data") % (partner.id,partner.name))
        if not partner.vat:
            raise except_orm(_('Advertencia'),_("La Empresa - (ID: %s) %s - no tiene el RFC definido, para usar esta empresato use this partner in Invoices this field must not be empty") % (partner.id,partner.name))
        return
    
    def create_ir_attachment_facturae(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attach = ''
        ir_attach_obj = self.pool.get('ir.attachment.facturae.mx')
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        attach_ids = []
        inv_type_facturae = {
            'out_invoice': True,
            'out_refund': True,
            'in_invoice': False,
            'in_refund': False}
        for invoice in self.browse(cr, uid, ids, context=context):            
            if inv_type_facturae.get(invoice.type, False):
                self.check_partner_data(cr, uid, invoice.partner_id, context=context)
                self.check_partner_data(cr, uid, invoice.address_issued_id, context=context)
                self.check_partner_data(cr, uid, invoice.company_emitter_id.address_invoice_parent_company_id, context=context)

                approval_id = invoice.invoice_sequence_id and invoice.invoice_sequence_id.approval_id or False
                if approval_id:
                    attach_ids.append( ir_attach_obj.create(cr, uid, {
                      'name': invoice.fname_invoice, 'invoice_id': invoice.id,
                      'type': invoice.invoice_sequence_id.approval_id.type},
                      context=None)#Context, because use a variable type of our code but we dont need it.
                    )
        if attach_ids:
            result = mod_obj.get_object_reference(cr, uid, 'l10n_mx_ir_attachment_facturae',
                                                            'action_ir_attachment_facturae_mx')
            id = result and result[1] or False
            result = act_obj.read(cr, uid, [id], context=context)[0]
            #choose the view_mode accordingly
            result['domain'] = "[('id','in',["+','.join(map(str, attach_ids))+"])]"
            result['res_id'] = attach_ids and attach_ids[0] or False
            res = mod_obj.get_object_reference(cr, uid, 'l10n_mx_ir_attachment_facturae', 
                                                            'view_ir_attachment_facturae_mx_form')
            result['views'] = [(res and res[1] or False, 'form')]
            return result
        return True

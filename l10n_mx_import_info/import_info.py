# -*- encoding: utf-8 -*-
# Author=Nhomar Hernandez nhomar@vauxoo.com
# Audited by=
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

from openerp.tools.translate import _
from openerp.osv import fields, osv


class import_info(osv.Model):
    _name = "import.info"
    _description = "Information about customs"
    _order = 'name asc'

    """
    def _get_audit(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        prod_obj = self.pool.get('product.product')
        for i in ids:
            chain = ''
            for p in self.browse(cr, uid, [i], context)[0].product_info_ids:
                if not self.browse(cr, uid, [i], context)[0].supplier_id.id in [
                    s.name.id for s in p.product_id.seller_ids]:
                    chain2 = '\nVerify the product: %s the Supplier on this document is not related to this product.\n' % p.product_id.name
                    chain = chain+chain2
            result[i] = chain
        return result

    """
    
    _columns = {
        'name'          : fields.char('Número Pedimento', 15,help="Número de Pedimento o Trámite", required=True),
        'customs'       : fields.char('Aduana', 64, help="Aduana usada para la importación de los productos", required=True),
        'date'          : fields.date('Fecha', help="Fecha del Pedimento", required=True),
        'package_ids'   : fields.one2many('stock.quant.package', 'import_id', 'Empaquetado'),
        'rate'          : fields.float('Tipo de Cambio', required=True, digits=(16, 4),help='Tipo de Cambio utilizado en el Pedimento Aduanal'),
        'company_id'    : fields.many2one('res.company', 'Compañía', required=True, select=1),
        'supplier_id'   : fields.many2one('res.partner', 'Agencia Aduanal', select=1, help="Agencia aduanal con la que se realizó el trámite de importación ..."),
        'invoice_ids'   : fields.many2many('account.invoice', 'account_invoice_rel', 'import_id', 'invoice_id', 'Facturas relacionadas'),
        #'product_info_ids': fields.one2many('product.import.info', 'import_id', 'Productos', required=False),
        'notes'         : fields.text('Observaciones'),
    }

    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'import.info', context=c)
    }

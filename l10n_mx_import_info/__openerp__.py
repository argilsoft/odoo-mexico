# -*- encoding: utf-8 -*-

{
    "name" : "Customs Information on lots",
    "version" : "0.1",
    "author" : "Argil Consulting",
    "category" : "Localization/Mexico",
    "website": "http://www.argil.mx",
    "description": """
Make relation between information of import with goverment.
With this module you will be able to make a relation between invoice and Information of importing transaction.
It will work as production lot make better control with quantities.
    """,
    "depends" : ["stock_account","account"],
    "demo" : [],
    "data" : [
        'security/ir.model.access.csv',
        'import_info_view.xml',
        #'product_view.xml',
        'stock_view.xml',
        #'label_report.xml',
        'security/groups.xml',
        'invoice_view.xml'
    ],
    "active": False,
    "installable": True
}

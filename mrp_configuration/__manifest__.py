# -*- coding: utf-8 -*-
{
    'name': "MRP Configuration",

    'summary': """
        This Module is use to MRP Configuration in the sale order. """,

    'description': """
        MRP Configuration
    """,

    'website': 'http://www.aktivsoftware.com',
    'author': 'Aktiv Software',
    'category': 'MRP',
    'version': '13.0.1.0.8',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'product', 'mrp', 'sale_margin'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/mrp_configuration_view.xml',
        'views/mrp_production_view.xml',
        'views/mrp_bom_view.xml',
        'views/product_view.xml',
        'views/stock_move_view.xml',
        'report/mrp_bom_config_report.xml',
        'report/mrp_bom_config_report_template.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
}

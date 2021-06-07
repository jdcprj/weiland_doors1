# -*- coding: utf-8 -*-
{
    'name': "Purchase Extension",

    'summary': """
        This Module is use to purchase Mail status after confirm the po. """,

    'description': """
        Purchase Extension
    """,

    'website': 'http://www.aktivsoftware.com',
    'author': 'Aktiv Software',
    'category': 'PURCHASE',
    'version': '13.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        'views/purchase_order_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
}

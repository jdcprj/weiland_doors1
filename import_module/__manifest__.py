# -*- coding: utf-8 -*-
{
    'name': "Import Customization",
    'summary': """
        This module contains all the customization which need for import the data. """,
    'description': """
	This module contains all the customization which need for import the data.
    """,
    'website': 'https://www.aktivsoftware.com/',
    'author': 'Aktivsoftware',
    'category': '',
    'version': '13.0.1.0.0',
    'depends': ['base','contacts', 'account'],
    'data': [
        'views/res_partner_views.xml',
        'views/account_payment_term_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
}

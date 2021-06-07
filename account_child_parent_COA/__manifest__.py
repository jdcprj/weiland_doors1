# -*- coding: utf-8 -*-
{
    'name': "COA Child Parent Relationship",

    'summary': """
        This Module is use to Add Child Parent Relationship in the COA. """,

    'description': """
        Add Child Parent Relationship in the COA
    """,

    'website': 'http://www.jdcsystems.net',
    'author': 'Khyati/Aktiv',
    'category': 'Account',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account_reports'],

    # always loaded
    'data': [
        'data/data_account_type.xml',
        'views/account_account.xml',
        'views/assets.xml',
        # 'wizard/update_customers_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}

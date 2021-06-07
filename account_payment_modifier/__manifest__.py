# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting Payment For Employee',
    'version': '13.0.1.0.0',
    'summary': """This module allow your users to create payment for employee.""",
    'description': """
        This module allows users to create payment for Employee
        request to stock picking.
    """,
    'author': 'Aktiv Software.',
    'website': 'http://www.aktivsoftware.com',
    'category': 'Accounting',
    'depends': [
        'purchase',
        'account',
        'sale',
        'sale_management',
        'hr',
        'sale_purchase'
    ],
    'data': [
        'data/emp_sequence.xml',
        'views/account_payment_view.xml',
    ],
    'installable': True,
    'application': False,
}

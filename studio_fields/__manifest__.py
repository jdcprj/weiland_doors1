# -*- coding: utf-8 -*-
{
    'name': "Studio Fields Customization",
    'summary': """
        This module contains all the customization which were created using studio. """,
    'description': """
        This module contains all the customization which were created using studio.
    """,
    'website': 'https://www.aktivsoftware.com/',
    'author': 'Aktivsoftware',
    'category': '',
    'version': '13.0.1.0.9',
    'depends': ['base','contacts', 'account',
    'sale_management', 'stock', 'mrp', 'product', 'stock_landed_costs',
    'stock_account', 'purchase', 'sale_crm', 'project', 'project_enterprise',
    'stock_picking_batch', 'purchase_requisition'],
    'data': [
        'security/ir.model.access.csv',
        'security/base_group.xml',

        'report/sale_quote_report.xml',
        # 'report/purchase_report_views.xml',
        'report/studio_report.xml',

        'data/mail_template_data.xml',
        'data/sale_order_mail_template.xml',

        'views/res_partner_views.xml',

        'views/mail_template_views.xml',

        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',

        'views/stock_move_views.xml',
        'views/stock_move_line_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_inventory_views.xml',

        'views/mrp_production_views.xml',
        'views/mrp_workorders_views.xml',
        'views/mrp_bom_line_views.xml',
        'views/mrp_routing_views.xml',
        'views/mrp_workcenter_views.xml',
        'views/mrp_bom_views.xml',

        'views/product_template_views.xml',
        'views/product_template_attribute_value_views.xml',
        'views/product_template_attribute_line_views.xml',
        'views/product_category_views.xml',
        'views/uom_category_views.xml',
        'views/uom_uom_views.xml',

        # 'views/product_product_views.xml',
        'views/product_supplierinfo_views.xml',
        'views/product_attribute_views.xml',
        'views/product_attribute_values_views.xml',

        'views/purchase_order_views.xml',
        'views/purchase_requisition_views.xml',
        # 'views/purchase_report_views.xml',

        'views/hr_employee_views.xml',

        'views/crm_lead_tag_views.xml',
        'views/crm_lead_views.xml',

        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
        'views/account_payment_views.xml',
        'views/account_account_views.xml',
        'views/account_bank_statement_views.xml',
        'views/account_bank_statement_line_views.xml',
        'views/account_online_provider_views.xml',

        'views/payment_acquirer_views.xml',

        'views/mail_message_views.xml',

        'views/studio_bids_views.xml',
        'views/studio_crm_views.xml',
        'views/studio_mrp_workorder_stage_views.xml',
        'views/studio_project_project_stage_views.xml',

        'views/action_views.xml',
        'views/menu_views.xml',

    ],
    'auto_install': False,
    'installable': True,
    'application': False
}

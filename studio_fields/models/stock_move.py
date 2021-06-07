from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_line_description = fields.Text(string="Sale line description",
        related="sale_line_id.name")
    job_name = fields.Char(string="Stock Move Job Name", related="group_id.sale_id.job_name")
    customer_name = fields.Char(string="Stock Move customer",
        related="group_id.sale_id.partner_id.display_name")
    job_production_id = fields.Many2one('mrp.production', string="Production SO2 job name")
    production_id_2 = fields.Many2one('mrp.production', string="Production ID")
    production_id_3 = fields.Many2one('mrp.production', string="Production")
    production_id_4 = fields.Many2one('mrp.production', string="Production")
    procurement_group_id = fields.Many2one(
        'procurement.group', string="Procurement Group")
    so_customer_id = fields.Many2one('res.partner', string="SO Customer",
        related="raw_material_production_id.sale_order_id.partner_id")
    so_job_name = fields.Char(string="SO Job Name", related="raw_material_production_id.sale_order_id.job_name")
    delivery_opening_number = fields.Char(string="Delivery Opening # (OPs)", related="sale_line_id.opening_number")
    new_field = fields.Integer(string="New Related Field",
        related="raw_material_production_id.sale_order_id.id")
    stock_invoice_status = fields.Selection(
        [('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'), ('no', 'Nothing to Invoice')],
        string="stock Invoice Status", related="raw_material_production_id.sale_order_id.invoice_status")
    new_field_2 = fields.Float(string="New Related Field")
    new_field_3 = fields.Char(string="New Related Field", 
        related='created_purchase_line_id.invoice_lines.partner_id.company_name')
    supplier_name = fields.Char(string="Supplier Name",
        related="product_tmpl_id.seller_ids.name.display_name")

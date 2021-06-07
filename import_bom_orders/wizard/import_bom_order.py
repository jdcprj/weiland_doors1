import base64
import xlrd
from odoo import models, fields


class ImportPurchaseOrderLine(models.TransientModel):
    _name = "import.bom.order"
    _description = "Import BOM Order"

    file_to_import = fields.Binary("File To Import", required=True)
    file_name = fields.Char("File Name", required=True)

    def import_data(self):
        for rec in self:
            read_file = base64.decodestring(rec.file_to_import)
            book = xlrd.open_workbook(file_contents=read_file)
            sheet = book.sheet_by_index(0)
            for line in range(1, sheet.nrows):
                row = sheet.row_values(line)
                if isinstance(row[0], float):
                    product_name = str(int(row[0]))
                else:
                    product_name = str(row[0])
                product = self.env['product.template'].sudo().search([('name', '=', product_name)])
                bom_order = self.env['mrp.bom'].sudo().search([('product_tmpl_id', '=', product.id)])
                if isinstance(row[4], float):
                    line_product_name = str(int(row[4]))
                else:
                    line_product_name = str(row[4])
                line_product = self.env['product.template'].sudo().search([('name', '=', line_product_name)])
                if not bom_order:
                    vals = {
                        'product_tmpl_id': product.id,
                        'code': str(row[1]),
                        'product_qty': row[2],
                        'type': str(row[3]),
                    }
                    bom_order = self.env['mrp.bom'].sudo().create(vals)
                    value_ids = self.env['product.attribute.value'].sudo()
                    if row[6]:
                        for value_name in row[6].split(","):
                            value = self.env['product.attribute.value'].sudo().search([
                                ('name', '=', value_name),
                                ('attribute_id', 'in', product.attribute_line_ids.attribute_id.ids)])
                            value_ids |= value.id
                    line_vals = {
                        'product_template_id': line_product.id,
                        'product_qty': row[5],
                        'product_uom_id': line_product.uom_po_id.id,
                        'bom_product_template_attribute_value_ids': [(6, 0, value_ids.ids)],
                        'bom_id': bom_order.id,
                    }
                    self.env['mrp.bom.line'].sudo().create(line_vals)
                    self.env.cr.commit()
                else:
                    value_ids = self.env['product.template.attribute.value'].sudo()
                    if row[6]:
                        for value_name in row[6].split(","):
                            value = self.env['product.attribute.value'].sudo().search([
                                ('name', '=', value_name), ('attribute_id', 'in', product.attribute_line_ids.attribute_id.ids)])
                            value_line = self.env['product.template.attribute.value'].sudo().search([
                                ('product_attribute_value_id', '=', value.id),
                                ('attribute_id', 'in', product.attribute_line_ids.attribute_id.ids),
                                ('product_tmpl_id', '=', product.id)])
                            value_ids |= value_line
                    line_vals = {
                        'product_template_id': line_product.id,
                        'product_qty': row[5],
                        'product_uom_id': line_product.uom_po_id.id,
                        'bom_product_template_attribute_value_ids': [(6, 0, value_ids.ids)],
                        'bom_id': bom_order.id,
                    }
                    lines = self.env['mrp.bom.line'].sudo().create(line_vals)
                    self.env.cr.commit()

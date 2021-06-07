import base64
import io
import xlsxwriter
import xlrd
from odoo import fields, models


class ProductVariantImportExport(models.TransientModel):
    _name = "wiz.product.variant.import.export"

    process = fields.Selection(selection=[
        ('export', 'Export'),
        ('import', 'Import')],
        string='Process', default="export")
    file_to_import = fields.Binary("File To Import")
    file_name = fields.Char("File Name")

    def perform_import_export_process(self):
        if self.process == 'export':
            fp = io.BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            sheet = workbook.add_worksheet("Product Variant Data")
            format = workbook.add_format({'align': 'center'})
            format.set_text_wrap()
            font_bold = workbook.add_format(
                {'align': 'center', 'bg_color': '#B8B8B8'})
            font_bold.set_bold()
            font_bold.set_text_wrap()
            row_frmt = workbook.add_format({'align': 'center'})
            row_frmt.set_font_size(10)
            sheet.set_default_row(24)
            title_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': 'white'})
            sheet.set_column('A:A', 10)
            sheet.set_column('B:C', 30)
            sheet.set_column('D:G', 20)
            rows = 0
            cols = 0
            sheet.write(rows, cols, 'ID.', title_format)
            cols += 1
            sheet.write(rows, cols, 'Product Name', title_format)
            cols += 1
            sheet.write(rows, cols, 'Attributes', title_format)
            cols += 1
            sheet.write(rows, cols, 'Sales Price', title_format)
            cols += 1
            sheet.write(rows, cols, 'Cost', title_format)
            cols += 1
            sheet.write(rows, cols, 'Quantity On Hand', title_format)
            cols += 1
            rows += 1
            products = self.env['product.product'].sudo().search([])
            for product in products:
                attributes = ""
                for attribute in product.product_template_attribute_value_ids:
                    attributes += attribute.display_name + "\n"
                cols = 0
                sheet.write(rows, cols, product.id, row_frmt)
                cols += 1
                sheet.write(rows, cols, product.name, row_frmt)
                cols += 1
                sheet.write(rows, cols, attributes.rstrip("\n"), row_frmt)
                cols += 1
                sheet.write(rows, cols, product.lst_price, row_frmt)
                cols += 1
                sheet.write(rows, cols, product.standard_price, row_frmt)
                cols += 1
                sheet.write(rows, cols, product.qty_available, row_frmt)
                rows += 1
            workbook.close()
            fp.seek(0)
            result = base64.b64encode(fp.read())
            attachment_obj = self.env['ir.attachment']
            attachment_id = attachment_obj.create({'name': 'Product variant.xlsx', 'datas': result})
            download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            return {
                "type": "ir.actions.act_url",
                "url": str(base_url) + str(download_url),
                "target": "new",
            }
        if self.process == 'import':
            read_file = base64.decodestring(self.file_to_import)
            book = xlrd.open_workbook(file_contents=read_file)
            sheet = book.sheet_by_index(0)
            for line in range(1, sheet.nrows):
                row = sheet.row_values(line)
                if isinstance(row[1], float):
                    part_number = int(row[0])
                else:
                    part_number = int(row[0])
                product = self.env['product.product'].sudo().search([('id', '=', part_number)])
                if product:
                    vals = {
                        'lst_price': row[3],
                        'standard_price': row[4],
                    }
                    product.sudo().write(vals)
                    self.env.cr.commit()

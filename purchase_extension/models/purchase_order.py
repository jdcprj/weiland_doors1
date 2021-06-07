from odoo import api,fields,models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    mail_status = fields.Selection([('sent', 'Sent'), ('not_sent', 'Not Sent')], string="Mail Status",
                                   default='not_sent')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_rfq_as_sent'):
            self.filtered(lambda o: o.state == 'draft').write({'state': 'sent'})
            self.filtered(lambda o: o.state == 'purchase').write({'mail_status': 'sent'})
        return super(PurchaseOrder, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

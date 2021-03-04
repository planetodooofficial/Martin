from odoo import models, fields, api, _

class MailTemplateInherit(models.Model):
    _inherit='mail.template'

    template_img = fields.Binary(string='Template Image')

    web_template = fields.Boolean('Website Template')


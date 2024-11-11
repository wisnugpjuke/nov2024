# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MaterialMaterial(models.Model):
    _name = 'material.material'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Material'
    _rec_name = 'material_name'

    active = fields.Boolean(default=True, tracking=True)
    material_code = fields.Char(required=True, tracking=True)
    material_name = fields.Char(required=True, tracking=True)
    material_type = fields.Selection([('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')], required=True, tracking=True)
    material_buy_price = fields.Monetary(currency_field='currency_id', required=True, tracking=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', index=True, required=True, tracking=True)
    company_id = fields.Many2one('res.company', index=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', index=True, related='company_id.currency_id')
    sync_statusCode = fields.Char('Status Code', tracking=True)
    sync_message = fields.Char('Message', tracking=True)
    sync_date = fields.Datetime('Date', tracking=True)

    _sql_constraints = [
        ("unique_material_code",
         "UNIQUE(material_code)",
         "Material Code already exist!"),
    ]

    @api.constrains('material_buy_price')
    def _check_material_buy_price(self):
        for rec in self:
            if rec.material_buy_price < 100:
                raise UserError(_("Material Buy Price can't below Rp 100"))

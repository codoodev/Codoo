# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Return(models.Model):
    _inherit = 'stock.picking'

    ret_receipt = fields.Many2one('rma.rma')
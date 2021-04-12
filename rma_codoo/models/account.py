# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Refund(models.Model):
    _inherit = 'account.move'

    ret_refund = fields.Many2one('rma.rma')

# -*- coding: utf-8 -*-

from odoo import models, fields


class POSConfig(models.Model):
    _inherit = 'pos.config'

    iface_orderline_order_notes = fields.Boolean(string='Orderline Notes', help='Allow custom notes on Orderlines.')

# -*- coding: utf-8 -*-
from odoo import models, fields, api


class employee_driver(models.Model):
    _inherit = 'hr.employee'

    is_driver = fields.Boolean('Driver')
    driver_unique_id = fields.Char('Driver Unique ID')
    driver_id = fields.Char('Driver ID')
    history = fields.One2many('traccar.report','device_id')

    @api.onchange('is_driver')
    def onch_is_driver(self):
        if not self.is_driver:
            self.driver_id = False

    def get_route(self):
        url = "%s" % self.env['config.traccar'].search([('id','=',1)]).server
        return {'name': 'Traccar',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url
                }

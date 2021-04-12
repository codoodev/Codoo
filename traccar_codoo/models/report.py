# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests


class TraccarReport(models.Model):
    _name = 'traccar.report'
    _rec_name = 'driver_name'

    report_id = fields.Char('Id')
    device_id = fields.Many2one('hr.employee',string='Driver',domain=[('is_driver', '=', True)])
    driver_name = fields.Char(related='device_id.name',string='Driver')
    latitude = fields.Char('Latitude')
    longitude = fields.Char('Longitude')
    date = fields.Datetime('Date')

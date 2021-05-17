# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from requests.auth import HTTPBasicAuth
import requests
from datetime import datetime


class ConfigTraccar(models.Model):
    _name = 'config.traccar'

    name = fields.Char()
    server = fields.Char('Server URL', required=True)
    token = fields.Char('Access Token', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)

    def check_drivers(self):
        url_users = '%s/api/devices?token=%s' %(self.server,self.token)
        user_token_response = requests.get(url_users, auth=HTTPBasicAuth(self.username, self.password))
        if str(user_token_response) == '<Response [200]>':
            for rec in user_token_response.json():
                self.env['hr.employee'].search([('driver_unique_id', '=', rec.get('uniqueId'))]).write({'driver_id':rec.get('id')})

    def action_get_data(self):
        self.check_drivers()
        date_now = datetime.now().strftime('%Y-%m-%d')

        url_device = '%s/api/devices?token=%s&devices' % (self.server,self.token)
        token_response_devices = requests.get(url_device, auth=HTTPBasicAuth(self.username, self.password))
        devices_list = []

        for rec_device in token_response_devices.json():
            devices_list.append(rec_device.get('id'))
        for driver in devices_list:
            url = '%s/api/reports/route?from=2019-03-25T00:00:00Z&to=2021-04-13T12:59:59Z&token=%s&deviceId=%s' % (self.server,self.token,driver)

            token_response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            if str(token_response) == '<Response [200]>':
                for rec in token_response.json():
                    date_format = "%s %s" %(rec.get('serverTime').split("T")[0],rec.get('serverTime').split("T")[1].split(".")[0])
                    date_server = datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S')
                    driver_id = self.env['hr.employee'].search([('driver_id', '=', rec.get('deviceId'))]).id
                    if not self.env['traccar.report'].search([('report_id','=',rec.get('id'))]):
                        self.env['traccar.report'].sudo().create({'report_id': rec.get('id'),
                                                                   'device_id': driver_id,
                                                                   'date': date_server,
                                                                   'latitude': rec.get('latitude'),
                                                                   'longitude': rec.get('longitude'),
                                                                   })

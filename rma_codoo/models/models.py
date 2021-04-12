# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Rma(models.Model):
    _name = 'rma.rma'

    name = fields.Char('Sequence', readonly=True, required=True, copy=False, default='New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('closed', 'Cancelled'),
        ], string='Status',
        copy=False, default='draft', readonly=True)

    subject = fields.Char('Subject', required=True)
    partner_id = fields.Many2one('res.partner',string='Partner', required=True, domain=[('customer_rank','>',0)])
    delivery_order = fields.Many2one('stock.picking',string='Delivery Order', required=True)
    date = fields.Date('Date',required=True, default=lambda self: fields.Date.today())
    rma_lines = fields.One2many('rma.lines','ram_ram')
    total_receipt = fields.Float(compute='_compute_receipt_quantity')
    total_refund = fields.Float(compute='_compute_refund_total_price')
    currency_id = fields.Many2one('res.currency',default= lambda self: self.env.user.company_id.currency_id)
    invoice_id = fields.Many2one('account.move')

    def _compute_receipt_quantity(self):
        for record in self:
            record.total_receipt = sum(self.env['stock.picking'].search(
                [('ret_receipt', '=', record.id)]).move_ids_without_package.mapped('quantity_done'))

    def _compute_refund_total_price(self):
        for record in self:
            record.total_refund = sum(self.env['account.move'].search(
                [('ret_refund', '=', record.id)]).mapped('amount_total'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('rma.seq') or 'New'
        result = super(Rma, self).create(vals)
        return result

    @api.onchange('partner_id')
    def onch_partner_id(self):
        name_deli = self.env['stock.picking'].search([('partner_id', '=', self.partner_id.id),('picking_type_code', '=','outgoing'), ('state', '=', 'done')])
        list_delivary = []
        for delv in name_deli:
            line_list = []
            line_list_return = []

            for line in delv.move_ids_without_package:
                line_list.append(line.quantity_done)

            name_deli_return = self.env['stock.picking'].search([('partner_id', '=', self.partner_id.id),('origin','=', 'Return of %s' % delv.name)])
            for ret in name_deli_return:
                for line_return in ret.move_ids_without_package:
                    line_list_return.append(line_return.quantity_done)
            if sum(line_list) > sum(line_list_return):
                list_delivary.append(delv.id)

        return {'domain': {'delivery_order': [('id', 'in', list_delivary)]}}

    @api.onchange('delivery_order')
    def onch_delivery_order(self):
        self.rma_lines = False
        lines_list = []
        returns = self.env['stock.picking'].search([('origin', '=', 'Return of %s' % self.delivery_order.name)])
        if self.delivery_order:
            invoice = self.env['account.move'].search([('invoice_origin','=',self.delivery_order.sale_id.name)], order='id')[-1]
            if invoice:
                self.invoice_id = invoice.id
        if self.delivery_order:
            if self.delivery_order.move_ids_without_package:
                for product in self.delivery_order.move_ids_without_package:
                    return_list = []
                    for rec in returns:
                        for line in rec.move_ids_without_package:
                            if product.product_id.id == line.product_id.id:
                                return_list.append(-line.quantity_done)
                    if (product.product_uom_qty + sum(return_list)) != 0.0:
                        lines_list.append((0, 0, {'product_id': product.product_id.id,
                                                  'delivered_quantity': product.product_uom_qty + sum(return_list),
                                                  # 'return_quantity': product.product_uom_qty
                                                  }))
        self.rma_lines = lines_list

    def approve(self):
        invoice = self.env['account.move'].search([('invoice_origin', '=', self.delivery_order.origin),('type','=','out_invoice')])
        refund = self.env['account.move'].search([])
        returns = self.env['stock.picking'].search([])
        sale_order = self.env['sale.order'].search([('name','=',self.delivery_order.origin)])
        invoice_line_list = []
        refund_line_list = []
        for inv_line in invoice.invoice_line_ids:

            for rma in self.rma_lines:
                if inv_line.product_id.id == rma.product_id.id and (rma.return_quantity > 0):
                    invoice_line_list.append((0, 0, {'product_id': rma.product_id.id,
                                                     'name': inv_line.name,
                                                     'account_id': inv_line.account_id.id,
                                                     'price_unit': inv_line.price_unit,
                                                     'quantity': rma.return_quantity,
                                                     }))
                    refund_line_list.append((0, 0, {'product_id': rma.product_id.id,
                                                    'product_uom_qty': rma.return_quantity,
                                                    'name': inv_line.name,
                                                    'product_uom': inv_line.product_uom_id.id,
                                                    }))

        refund.create({'partner_id': invoice.partner_id.id,
                       'ref': self.name,
                       'ret_refund':self.id,
                       'type': 'out_refund',
                       'user_id': invoice.user_id.id,
                       'team_id': invoice.team_id.id,
                       'invoice_origin': invoice.name,
                       'journal_id': invoice.journal_id.id,
                       'invoice_line_ids': invoice_line_list
                       })

        returns.create({'partner_id': invoice.partner_id.id,
                        'origin': 'Return of %s' % self.delivery_order.name,
                        'ret_receipt': self.id,
                        'picking_type_id': self.env['stock.picking.type'].search([('warehouse_id','=',sale_order.warehouse_id.id),('code','=','incoming')]).id,
                        'location_dest_id': self.env['stock.picking.type'].search([('warehouse_id','=',sale_order.warehouse_id.id),('code','=','incoming')]).default_location_dest_id.id,
                        'location_id': self.partner_id.property_stock_customer.id,
                        'move_ids_without_package': refund_line_list,
                        })

        self.write({'state': 'approved'})

    def action_view_credit_note(self):
        template_tree = self.env.ref('account.view_invoice_tree')
        template_form = self.env.ref('account.view_move_form')

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'name': 'Credit note',
            'res_model': 'account.move',
            'view_id': template_tree.id,
            'views': [(template_tree.id, 'tree'),(template_form.id, 'form')],

            'domain': [('ret_refund', '=', self.id)],
            'target': 'current'
        }

    def action_view_recipt(self):
        template_tree = self.env.ref('stock.vpicktree')
        template_form = self.env.ref('stock.view_picking_form')

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'name': 'Receipt',
            'res_model': 'stock.picking',
            'view_id': template_tree.id,
            'views': [(template_tree.id, 'tree'), (template_form.id, 'form')],

            'domain': [('ret_receipt', '=', self.id)],
            'target': 'current'
        }

    def reject(self):
        self.write({'state': 'closed'})


class RmaLines(models.Model):
    _name = 'rma.lines'

    ram_ram = fields.Many2one('rma.rma')
    product_id = fields.Many2one('product.product')
    delivered_quantity = fields.Float('Delivered Quantity')
    return_quantity = fields.Float('Return Quantity')
    reason = fields.Many2one('rma.reason')


class RmaReason(models.Model):
    _name = 'rma.reason'

    name = fields.Char('Reason')

# -*- coding: utf-8 -*-
from odoo import fields, models


class VideoclubRental(models.Model):
    _name = 'videoclub.rental'
    _description = 'Rental of a tape'
    _order = 'rental_date desc'

    tape_id = fields.Many2one('videoclub.tape', string='Tape', required=True, ondelete='cascade')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)

    rental_date = fields.Date(string='Rental date', default=fields.Date.context_today, required=True)
    expected_return_date = fields.Date(string='Expected return date')
    actual_return_date = fields.Date(string='Actual return date')

    state = fields.Selection([
        ('active', 'Active'),
        ('returned', 'Returned'),
    ], string='State', default='active', required=True)
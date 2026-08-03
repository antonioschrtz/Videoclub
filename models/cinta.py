# -*- coding: utf-8 -*-
from odoo import api, fields, models


class VideoclubTape(models.Model):
    _name = 'videoclub.tape'
    _description = 'Movie tape'

    movie_id = fields.Many2one('videoclub.movie', string='Movie', ondelete='set null')
    state = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
    ], string='State', default='available')

    expected_return_date = fields.Date(
        string='Expected return date',
        compute='_compute_expected_return_date',
        store=False,
    )

    rental_ids = fields.One2many(
        'videoclub.rental',
        'tape_id',
        string='Rental history',
    )

    @api.depends('rental_ids.state', 'rental_ids.expected_return_date')
    def _compute_expected_return_date(self):
        # Shows the return deadline of the active rental, when rented.
        for tape in self:
            active_rentals = tape.rental_ids.filtered(lambda rental: rental.state == 'active')
            tape.expected_return_date = active_rentals[:1].expected_return_date or False
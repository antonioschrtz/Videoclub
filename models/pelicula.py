# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models


class VideoclubMovie(models.Model):
    _name = 'videoclub.movie'
    _description = 'Movie'

    name = fields.Char(string='Title', required=True)
    director_id = fields.Many2one('videoclub.director', string='Director')
    genre_ids = fields.Many2many('videoclub.genre', string='Genres')
    tapes_ids = fields.One2many('videoclub.tape', 'movie_id', string='Tapes')

    # Computed fields
    num_tapes = fields.Integer(string='Number of tapes', compute='_compute_tape_stats', store=True)
    num_available = fields.Integer(string='Available tapes', compute='_compute_tape_stats', store=True)
    availability_date = fields.Date(string='Availability date', compute='_compute_tape_stats', store=True)
    has_rented = fields.Boolean(string='I have rented it', compute='_compute_is_rented_by_me', store=False)
    rent_state = fields.Selection([
        ('rent', 'Alquilar'),
        ('return', 'Devolver'),
        ('unavailable', 'No disponible'),
    ], string='Rent action', compute='_compute_rent_state', store=False)

    @api.depends('tapes_ids.state', 'tapes_ids.rental_ids.state', 'tapes_ids.rental_ids.expected_return_date')
    def _compute_tape_stats(self):
        today = fields.Date.context_today(self)
        for movie in self:
            tapes = movie.tapes_ids
            movie.num_tapes = len(tapes)
            movie.num_available = len(tapes.filtered(lambda tape: tape.state == 'available'))

            active_rentals = tapes.rental_ids.filtered(lambda rental: rental.state == 'active')
            dates = [date for date in active_rentals.mapped('expected_return_date') if date]
            if movie.num_available > 0:
                movie.availability_date = today
            else:
                movie.availability_date = min(dates) if dates else False

    @api.depends('tapes_ids.rental_ids.customer_id', 'tapes_ids.rental_ids.state')
    @api.depends_context('uid')
    def _compute_is_rented_by_me(self):
        partner = self.env.user.partner_id
        for movie in self:
            rentals = movie.tapes_ids.rental_ids.filtered(
                lambda rental: rental.customer_id.id == partner.id and rental.state == 'active'
            )
            movie.has_rented = bool(rentals)

    @api.depends('has_rented', 'num_available')
    @api.depends_context('uid')
    def _compute_rent_state(self):
        # Determines which button to show for the current user.
        for movie in self:
            if movie.has_rented:
                movie.rent_state = 'return'
            elif movie.num_available > 0:
                movie.rent_state = 'rent'
            else:
                movie.rent_state = 'unavailable'

    def action_rent_movie(self):
        # Creates an active rental for an available tape of the current partner.
        partner = self.env.user.partner_id
        rental_date = fields.Date.context_today(self)
        for movie in self:
            tape = movie.tapes_ids.filtered(lambda item: item.state == 'available')[:1] #Avoid IndexError if no available tapes
            if not tape:
                continue
            self.env['videoclub.rental'].create({
                'tape_id': tape.id,
                'customer_id': partner.id,
                'rental_date': rental_date,
                'expected_return_date': rental_date + timedelta(days=7),
            })
            tape.state = 'rented'
        return True

    def action_return_movie(self):
        # Closes the active rentals of the current customer for this movie.
        partner = self.env.user.partner_id
        for movie in self:
            active_rentals = movie.tapes_ids.rental_ids.filtered(
                lambda rental: rental.customer_id.id == partner.id and rental.state == 'active'
            )
            for rental in active_rentals:
                rental.write({
                    'state': 'returned',
                    'actual_return_date': fields.Date.context_today(self),
                })
                rental.tape_id.state = 'available'
        return True

    def action_manage(self):
        # Applies the action directly according to the current rental state.
        self.ensure_one()
        if self.rent_state == 'return':
            return self.action_return_movie()
        if self.rent_state == 'rent':
            return self.action_rent_movie()
        # Unavailable: nothing to do.
        return True
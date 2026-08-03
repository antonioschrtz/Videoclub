# -*- coding: utf-8 -*-
from odoo import fields, models


class VideoclubMovieWizard(models.TransientModel):
    _name = 'videoclub.movie_wizard'
    _description = 'Search movies by genres'

    genre_ids = fields.Many2many('videoclub.genre', string='Genres')

    def action_search(self):
        # Filters the movies that contain ALL the selected genres at once.
        selected = self.genre_ids
        matching = self.env['videoclub.movie'].search([]).filtered(
            lambda movie: all(genre in movie.genre_ids for genre in selected)
        )
        return {
            'type': 'ir.actions.act_window',
            'name': 'Movies by genres',
            'res_model': 'videoclub.movie',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', matching.ids)],
        }
# -*- coding: utf-8 -*-
from odoo import fields, models


class VideoclubDirector(models.Model):
    _name = 'videoclub.director'
    _description = 'Movie director'

    name = fields.Char(string='Name', required=True)
    nationality = fields.Char(string='Nationality')

    movie_ids = fields.One2many('videoclub.movie', 'director_id', string='Movies')
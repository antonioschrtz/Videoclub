# -*- coding: utf-8 -*-
from odoo import fields, models


class VideoclubGenre(models.Model):
    _name = 'videoclub.genre'
    _description = 'Movie genre'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
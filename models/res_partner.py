from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_director = fields.Boolean(string="Is director", default=False)
    movie_ids = fields.One2many("videoclub.movie", "director_id", string="Movies")

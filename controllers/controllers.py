# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Videoclub(http.Controller):

    @http.route('/videoclub', type='http', auth='public', website=False)
    def catalog(self, **kw):
        movies = request.env['videoclub.movie'].search([], order='name')
        selection = request.env['videoclub.movie'].fields_get(['rent_state'])['rent_state']['selection']
        labels = dict(selection)
        data = [{
            'id': m.id,
            'name': m.name,
            'director': m.director_id.name,
            'num_available': m.num_available,
            'state_label': labels.get(m.rent_state, m.rent_state),
        } for m in movies]
        return request.render('videoclub.catalog', {
            'movies': data,
            'csrf_token': request.csrf_token(),
            'logged': not request.env.user._is_public(),
        })

    @http.route('/videoclub/manage/<int:movie_id>', type='http', auth='user', methods=['POST'])
    def manage(self, movie_id, **kw):
        movie = request.env['videoclub.movie'].browse(movie_id).exists()
        if movie:
            movie.action_manage()
        return request.redirect('/videoclub')
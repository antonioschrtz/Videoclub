# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestTapeViews(TransactionCase):

    def test_tape_tree_order_and_context(self):
        movie = self.env['videoclub.movie'].create({'name': 'Example Movie'})
        tape = self.env['videoclub.tape'].create({'movie_id': movie.id, 'state': 'available'})

        action = self.env.ref('videoclub.action_videoclub_tape')
        self.assertEqual(action.view_mode, 'tree,form')
        self.assertEqual(action.context.get('group_by'), 'movie_id')

        view = self.env['ir.ui.view'].search([
            ('model', '=', 'videoclub.tape'),
            ('type', '=', 'tree'),
            ('name', '=', 'videoclub.tape.tree')
        ], limit=1)
        self.assertTrue(view.id)
        self.assertIn('state', view.arch)

        self.assertEqual(tape.movie_id.id, movie.id)

    def test_movie_director_relation(self):
        director = self.env['videoclub.director'].create({
            'name': 'Director A',
            'nationality': 'Spanish',
        })
        movie = self.env['videoclub.movie'].create({'name': 'Movie B', 'director_id': director.id})

        self.assertEqual(movie.director_id.id, director.id)
        self.assertEqual(director.movie_ids, movie)

    def test_movie_button_state(self):
        partner = self.env.user.partner_id
        movie = self.env['videoclub.movie'].create({'name': 'Movie C'})
        tape = self.env['videoclub.tape'].create({'movie_id': movie.id, 'state': 'available'})

        # Available tape and not rented -> show "Rent".
        self.assertEqual(movie.rent_state, 'rent')

        # Rent it -> movie is rented by current user -> show "Return".
        movie.action_rent_movie()
        self.assertEqual(movie.rent_state, 'return')
        self.assertEqual(tape.state, 'rented')

        # Return it -> back to available -> show "Rent".
        movie.action_return_movie()
        self.assertEqual(movie.rent_state, 'rent')
        self.assertEqual(tape.state, 'available')

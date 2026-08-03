# -*- coding: utf-8 -*-
# from odoo import http


# class Videoclub(http.Controller):
#     @http.route('/videoclub/videoclub', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/videoclub/videoclub/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('videoclub.listing', {
#             'root': '/videoclub/videoclub',
#             'objects': http.request.env['videoclub.videoclub'].search([]),
#         })

#     @http.route('/videoclub/videoclub/objects/<model("videoclub.videoclub"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('videoclub.object', {
#             'object': obj
#         })

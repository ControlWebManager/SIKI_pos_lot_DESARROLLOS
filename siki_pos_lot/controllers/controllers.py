# -*- coding: utf-8 -*-
from openerp import http

# class SikiPosLot(http.Controller):
#     @http.route('/siki_pos_lot/siki_pos_lot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/siki_pos_lot/siki_pos_lot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('siki_pos_lot.listing', {
#             'root': '/siki_pos_lot/siki_pos_lot',
#             'objects': http.request.env['siki_pos_lot.siki_pos_lot'].search([]),
#         })

#     @http.route('/siki_pos_lot/siki_pos_lot/objects/<model("siki_pos_lot.siki_pos_lot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('siki_pos_lot.object', {
#             'object': obj
#         })
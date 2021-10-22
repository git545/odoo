# -*- coding: utf-8 -*-
from odoo import http


# class Pract1(http.Controller):
#     @http.route('/pract1/pract1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pract1/pract1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pract1.listing', {
#             'root': '/pract1/pract1',
#             'objects': http.request.env['pract1.pract1'].search([]),
#         })

#     @http.route('/pract1/pract1/objects/<model("pract1.pract1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pract1.object', {
#             'object': obj
#         })

class demo(http.Controller):
      @http.route('/pract1/demo',auth='public')
      def index(self,**kw):
          return "Hello world erp..."

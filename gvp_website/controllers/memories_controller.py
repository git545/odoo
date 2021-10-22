import werkzeug
from odoo import http
import random
import base64

from flask import Flask, flash,render_template, request
from werkzeug.utils import secure_filename
import os
import pathlib
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
path = os.getcwd()
UPLOAD_FOLD = path+'/dev/custom/gvp_website/static/photos'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config[ 'UPLOAD_FOLDER' ] = UPLOAD_FOLDER
app.config[ 'PATH' ]='gvp_website/static/photos'

class Memories(http.Controller):

    @http.route([ '/cralbum' ], type='http', auth="user", website=True)
    def Add_memories(self, context=None, **kwargs):
        uid = str(http.request.session.uid)
        start_year = http.request.env['tbl_year'].search([])
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.memory_temp',
                                   {
                                       'basic_prof_p': basic_prof_home,
                                       'to_year_dd': start_year,
                                       'from_month': [ "January", "February", "March", "April", "May", "June", "July",
                                                       "August", "September", "October", "November", "December" ],
                                    })

    @http.route('/album',methods=[ 'POST', 'GET' ], type="http", auth="user", website=True, csrf=False)
    def album_upload(self, **kwargs):
        uid = http.request.session.uid
        with app.test_request_context():
            if http.request.env["tbl_memories"].sudo().search([("album_name", "=", kwargs.get("txt_albumname"))]):
                return http.request.render('gvp_website.errpage', {'album_error': "Album name already exits", })
            else:
                f = kwargs.get("album_img")
                file_extension = pathlib.Path(f.filename).suffix
                n = random.randint(0, 99999)
                pname = str(uid) + str(n) + file_extension
                pic_path = os.path.join(app.config[ 'UPLOAD_FOLDER' ], secure_filename(pname))
                f.save(os.path.join(app.config[ 'UPLOAD_FOLDER' ], secure_filename(pname)))
                with open(pic_path, "rb") as img_file:
                    my_string = base64.b64encode(img_file.read())
                    basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
                    http.request.env[ 'tbl_memories' ].create({
                        'userid': http.request.session.uid,
                        'album_name': kwargs.get("txt_albumname"),
                        'album_month': kwargs.get("month_to1"),
                        'album_year': kwargs.get("year_to1"),
                        'album_img': my_string,

                    })
        return http.request.render('gvp_website.save_album',{'basic_prof_p': basic_prof_home,})
    @http.route('/viewalbum',type="http",auth="user",csrf=False,website=True)
    def album_view(self, **kwargs):
        uid = http.request.session.uid

        album_get= http.request.env[ 'tbl_memories' ].search([])
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.view_album', {
            'album_get':album_get,
            'basic_prof_p': basic_prof_home,
        })
    @http.route('/addmore',methods=[ 'POST', 'GET' ], type="http", auth="user", website=True, csrf=False)
    def add_more_img_upload(self,**kwargs):
        uid = http.request.session.uid
        with app.test_request_context():
                aid = http.request.session['memid']
                f = kwargs.get("album_img_more")
                file_extension = pathlib.Path(f.filename).suffix
                n = random.randint(0, 99999)
                pname = str(uid) + str(n) + file_extension
                pic_path = os.path.join(app.config[ 'UPLOAD_FOLDER' ], secure_filename(pname))
                f.save(os.path.join(app.config[ 'UPLOAD_FOLDER' ], secure_filename(pname)))
                with open(pic_path, "rb") as img_file:
                    my_string = base64.b64encode(img_file.read())
                    basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])

                    http.request.env[ 'tbl_album' ].create({
                        'userid': http.request.session.uid,
                        'album_desc': kwargs.get("txt_desc"),
                        'mem_id' : aid,
                        'album_photo': my_string
                    })
        return http.request.render('gvp_website.save_album',{'basic_prof_p': basic_prof_home,})

    @http.route('/viewalbum/<model("tbl_memories"):memories>', type="http", auth="user", csrf=False, website=True)
    def memories(self, memories):
        return http.request.render('gvp_website.add_album_img', {
            'album': memories
        })

    @http.route('/viewalbum/<int:mem_id>/<string:status>', type="http", auth='user', csrf=False, Website=True)
    def album_ref_id(self, mem_id, status, **kwargs):
        uid = http.request.session.uid
        http.request.session[ 'memid' ]=mem_id
        get_cnt = http.request.env[ 'tbl_album' ].search_count([ ('mem_id', '=', mem_id) ])
        get_memories_album=http.request.env[ 'tbl_album' ].search([ ('mem_id', '=', mem_id) ])
        get_album_name = http.request.env[ 'tbl_memories' ].search([ ('id', '=', mem_id) ])
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        http.request.env[ 'tbl_memories' ].search([ ('id', '=', mem_id) ]).write({'cnt':get_cnt})
        return http.request.render('gvp_website.add_album_img',
                                   {'get_memories_album':get_memories_album,
                                    'get_album_name':get_album_name,
                                    'basic_prof_p': basic_prof_home,
                                    })

    @http.route('/all_memory', type="http", auth="user", csrf=False, website=True)
    def album_all_memory(self, **kwargs):
        uid = http.request.session.uid
        album_get = http.request.env[ 'tbl_memories' ].search([ ])
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.all_memory', {
            'album_get': album_get,
            'basic_prof_p': basic_prof_home,
        })

    @http.route('/albums_del/<int:al_id>/<string:status>', type="http", auth='user', csrf=False, Website=True)
    def albums_record_delete(self, al_id, status, **kwargs):
        http.request.env[ 'tbl_album' ].search([ ('id', '=', al_id) ]).unlink()
        return http.request.render('gvp_website.album_more_del_page')
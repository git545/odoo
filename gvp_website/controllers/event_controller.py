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

class Events(http.Controller):

    @http.route([ '/crevent' ], type='http', auth="user", website=True)
    def Add_Event(self, context=None, **kwargs):
        uid = str(http.request.session.uid)
        for i in range(1, 60):
         print(i)
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.event_temp',
                                   {
                                       'event_hours': [ "01", "02", "03", "04", "05", "06", "07",
                                                       "08", "09", "10", "11", "12" ],
                                       'event_min': i,
                                       'event_ampm':['AM','PM'],
                                       'basic_prof_p': basic_prof_home,
                                   })

    @http.route('/event',methods=[ 'POST', 'GET' ], type="http", auth="user", website=True, csrf=False)
    def create_event(self, **kwargs):
        uid = http.request.session.uid
        with app.test_request_context():
            if http.request.env["tbl_event"].sudo().search([("event_title", "=", kwargs.get("txt_eventtitle"))]):
                return http.request.render('gvp_website.event_error', {'album_error': "event name already exits", })
            else:
                    basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
                    etime=kwargs.get("event_time_hours")+":"+kwargs.get("event_time_min")+" "+kwargs.get("event_time_ampm")
                    f = kwargs.get("event_img")
                    file_extension = pathlib.Path(f.filename).suffix
                    n = random.randint(0, 99999)
                    pname = str(uid) + str(n) +kwargs.get("txt_eventtitle")+ file_extension
                    pic_path = os.path.join(app.config[ 'UPLOAD_FOLDER' ], secure_filename(pname))
                    f.save(os.path.join(app.config[ 'UPLOAD_FOLDER' ], secure_filename(pname)))
                    with open(pic_path, "rb") as img_file:
                        my_string = base64.b64encode(img_file.read())
                        http.request.env[ 'tbl_event' ].create({
                            'userid': http.request.session.uid,
                            'event_title': kwargs.get("txt_eventtitle"),
                            'event_startdate': kwargs.get("txt_startdate"),
                            'event_enddate': kwargs.get("txt_enddate"),
                            'event_time': etime,
                             'event_url' :  kwargs.get("url"),
                            'event_desc': kwargs.get("txtEditor"),
                            'event_img' : my_string,
                           })
                        return http.request.render('gvp_website.save_event',{'basic_prof_p': basic_prof_home,})
    @http.route('/viewevent',type="http",auth="user",csrf=False,website=True)
    def event_view(self, **kwargs):
        uid = http.request.session.uid
        event_get= http.request.env[ 'tbl_event' ].search([])
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.view_event', {
            'event_get':event_get,
            'basic_prof_p': basic_prof_home,
        })
    @http.route('/viewevent/<int:eid>/<string:status>', type="http", auth='user', csrf=False, Website=True)
    def event_ref_id(self, eid, status, **kwargs):
        uid = http.request.session.uid
        http.request.session[ 'eid' ]=eid
        get_event_detail = http.request.env[ 'tbl_event' ].search([ ('id', '=', eid) ])
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.view_details',
                                   {'get_event_detail':get_event_detail,
                                    'basic_prof_p': basic_prof_home,
                                    })

    @http.route('/allevent', type="http", auth="user", csrf=False, website=True)
    def event_all_event(self, **kwargs):
        uid = http.request.session.uid
        event_get = http.request.env[ 'tbl_event' ].search([ ])

        return http.request.render('gvp_website.all_event', {
            'event_get': event_get,

        })

    @http.route('/event_del/<int:event_id>/<string:status>', type="http", auth='user', csrf=False, Website=True)
    def events_record_delete(self, event_id, status, **kwargs):
        http.request.env[ 'tbl_event' ].search([ ('id', '=', event_id) ]).unlink()
        return http.request.render('gvp_website.even_del_page')
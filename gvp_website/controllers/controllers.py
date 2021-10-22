# -*- coding: utf-8 -*-
import base64
from datetime import date
from odoo import http
import psycopg2
from flask import Flask, flash,render_template, request
from werkzeug.utils import secure_filename
import os
import pathlib
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['UPLOAD_PATH'] = 'photos/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
path = os.getcwd()
UPLOAD_FOLD = path+'/dev/custom/gvp_website/static/photos'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config[ 'UPLOAD_FOLDER' ] = UPLOAD_FOLDER
app.config[ 'PATH' ]='gvp_website/static/photos'
class GvpWebsite(http.Controller):
    @http.route('/home', type="http", auth="user", website=True)
    def home_init(self, **kwargs):
        uid = str(http.request.session.uid)
        conn = psycopg2.connect(database="gvpodoo", user='sanjay', password='545', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()
        SQL_QUERY = 'Insert into tbl_basicinfo(userid,fname,profile_photo) SELECT r.id,0,0 from res_users r WHERE NOT EXISTS ( SELECT b.userid FROM tbl_basicinfo b WHERE b.userid = r.id) and r.id=' + uid + ''
        cursor.execute(SQL_QUERY)

        SQL_QUERY_WORK = 'Insert into tbl_work(userid) SELECT r.id from res_users r WHERE NOT EXISTS ( SELECT b.userid FROM tbl_work b WHERE b.userid = r.id) and r.id=' + uid + ''
        cursor.execute(SQL_QUERY_WORK)
        conn.commit()
        conn.close()
        return http.request.render('gvp_website.home')
    # @http.route('/home', type="http",auth="user",website=True)
    # def home(self, **kwargs):
    #     uid = str(http.request.session.uid)
    #
    #     return http.request.render('gvp_website.home')

    @http.route(['/my','/my/home/'], type='http', auth="user", website=True)
    def user_profiles(self , context=None ,**kwargs):
        #partner = http.request.env['res.users'].browse(http.request.env.uid).partner_id
        uid = str(http.request.session.uid)
        conn = psycopg2.connect(database="gvpodoo", user='sanjay', password='545', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()
        SQL_QUERY = 'Insert into tbl_basicinfo(userid,fname,profile_photo) SELECT r.id,0,0 from res_users r WHERE NOT EXISTS ( SELECT b.userid FROM tbl_basicinfo b WHERE b.userid = r.id) and r.id=' + uid + ''
        cursor.execute(SQL_QUERY)

        SQL_QUERY_WORK = 'Insert into tbl_work(userid) SELECT r.id from res_users r WHERE NOT EXISTS ( SELECT b.userid FROM tbl_work b WHERE b.userid = r.id) and r.id=' + uid + ''
        cursor.execute(SQL_QUERY_WORK)
        conn.commit()
        conn.close()
        partner = http.request.env.user.partner_id
        basic_prof_p = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        user_prof_p = http.request.env['res.partner'].search([('id', '=', partner.id)])
        edu_prof_p = http.request.env[ 'tbl_education' ].search([ ('userid', '=', uid) ])
        work_prof_p = http.request.env[ 'tbl_exp' ].search([ ('userid', '=', uid) ])
        cur_prof_p = http.request.env[ 'tbl_work' ].search([ ('userid', '=', uid) ])
        # if http.request.env[ "tbl_basicinfo" ].sudo().search([ ('fname', '=', False) ]):
        #     return http.request.render('gvp_website.home')
        # else:
        return http.request.render('gvp_website.myprof',
                                   {'users_profile_p': user_prof_p,
                                    'edu_profile_p': edu_prof_p,
                                    'basic_prof_p': basic_prof_p,
                                    'work_profile_p': work_prof_p,
                                    'current_profile_p': cur_prof_p,
                                    })
    @http.route('/edu',type="http",auth="user",csrf=False,website=True)
    def education_profile(self, **kwargs):
        td = date.today()
        for i in range(1,50):
            print(i)
        start_year = http.request.env['tbl_year'].search([])
        countries = http.request.env[ 'tbl_country' ].search([ ])
        university_name_search = http.request.env[ 'tbl_uni_name' ].search([])
        course_name_search = http.request.env[ 'tbl_course' ].search([])
        Area_name_search = http.request.env[ 'tbl_functional_area' ].search([ ])
        Industry_name_search = http.request.env[ 'tbl_industry' ].search([ ])
        uid = http.request.session.uid
        basic_edit_update= http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        work_edit_update = http.request.env[ 'tbl_work' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.registration_form', {
            'base_edit_data':basic_edit_update,
            'workprof_edit_data': work_edit_update,
            'from_year_dd': start_year,
            'university_name':university_name_search,
            'course_name': course_name_search,
            'industry_name': Industry_name_search,
            'area_name': Area_name_search,
            'to_year_dd': start_year,
            'relevant_exp':i,
            'countries':countries,
            'from_month':["January","February","March","April","May","June","July","August","September","October","November","December"],
        })

    @http.route('/profile/edu', type="http", auth="user", csrf=False, website=True)
    def education_submit(self, **kwargs):
        uid= http.request.session.uid
        wt = http.request.env[ 'tbl_basicinfo' ]
        id_needed = wt.search([ ('userid', '=', uid) ]).id
        new = wt.browse(id_needed)
        list1 = new.id
        http.request.env['tbl_education'].create({
            'userid':  http.request.session.uid,
            'bparent_id':list1,
            'instname': kwargs.get("txtInst_name"),
            'uniname': kwargs.get("txtUni_name"),
            'course': kwargs.get("txt_course"),
            'fmonth': kwargs.get("month_from1"),
            'fyear': kwargs.get("year_from1"),
            'tmonth': kwargs.get("month_to1"),
            'tyear': kwargs.get("year_to1"),
             'chkstudy': kwargs.get("chkstudy"),
            })
        return http.request.render('gvp_website.save_page')

    @http.route('/exp', type="http", auth="user", csrf=False, website=True)
    def exp_submit(self, **kwargs):
        uid = http.request.session.uid
        wt = http.request.env[ 'tbl_basicinfo' ]
        id_needed = wt.search([ ('userid', '=', uid) ]).id
        new = wt.browse(id_needed)
        list1 = new.id
        http.request.env[ 'tbl_exp' ].create({
            'userid': http.request.session.uid,
            'bparent_id': list1,
            'orgname': kwargs.get("txt_org"),
            'desg': kwargs.get("txt_designation"),
            'loc': kwargs.get("txt_location"),
            'fmonth': kwargs.get("month_from_exp1"),
            'fyear': kwargs.get("from_year_exp2"),
            'tmonth': kwargs.get("month_exp_to1"),
            'tyear': kwargs.get("year_exp_to1"),
            'chkwork': kwargs.get("chkwork"),
        })
        return http.request.render('gvp_website.save_page')

    @http.route('/basic', type="http",auth='user', csrf=False,Website=True)
    def basicinfo_submit(self, **kwargs):
        uid=http.request.session.uid
        basicdata =  http.request.env['tbl_basicinfo'].search([('userid', '=', uid)])
        basicdata.write({
            'fname': kwargs.get("txt_firstname"),
            'lname': kwargs.get("txt_lastname"),
            'dob': kwargs.get("txtdob"),
            'mobile': kwargs.get("mobileno"),
            'pemail': kwargs.get("Personal_email"),
            'aemail': kwargs.get("alt_email"),
            'gender': kwargs.get("rd_gender"),
            'addr' : kwargs.get("txtaddress"),
            'city': kwargs.get("txtcity"),
            'pincode': kwargs.get("txtpincode"),
            'statename': kwargs.get("txtstate"),
            'countryname': kwargs.get("txtcountry"),
            })
        return http.request.render('gvp_website.save_page')

    @http.route('/work', type="http", auth='user', csrf=False, Website=True)
    def workinfo_submit(self, **kwargs):
        uid = http.request.session.uid
        wt = http.request.env[ 'tbl_basicinfo' ]
        id_needed = wt.search([ ('userid', '=', uid) ]).id
        new = wt.browse(id_needed)
        list1 = new.id
        basicdata = http.request.env[ 'tbl_work' ].search([ ('userid', '=', uid) ])
        basicdata.write({
            'bparent_id': list1,
            'farea': kwargs.get("txt_arealist"),
            'skills': kwargs.get("txt_skills"),
            'rexp': kwargs.get("rexpr_from_id"),
            'industry': kwargs.get("txt_industry"),
        })
        return http.request.render('gvp_website.save_page')
    @http.route('/edu_delete/<int:edu_id>/<string:status>', type="http",auth='user', csrf=False,Website=True)
    def edu_record_delete(self, edu_id, status, **kwargs):
        http.request.env['tbl_education'].search([('id', '=', edu_id)]).unlink()
        return http.request.render('gvp_website.del_page')

    @http.route('/exp_delete/<int:exp_id>/<string:status>', type="http",auth='user', csrf=False,Website=True)
    def exp_record_delete(self, exp_id, status, **kwargs):
        http.request.env['tbl_exp'].search([('id', '=', exp_id)]).unlink()
        return http.request.render('gvp_website.del_page')


    @http.route('/uploadd', methods=[ 'post', 'get' ], type="http", auth="user", website=True, csrf=False)
    def upload(self, **kwargs):
        uid = http.request.session.uid
        with app.test_request_context():
            f=kwargs.get("photo")

            file_extension = pathlib.Path(f.filename).suffix
            pname=str(uid)+file_extension
            oldfile=(os.path.join(app.config[ 'UPLOAD_FOLDER' ],secure_filename (f.filename)))
            newfile=(os.path.join(app.config[ 'UPLOAD_FOLDER' ],secure_filename (pname)))
            #os.rename(oldfile,newfile)
            static_path = os.path.join(app.config[ 'PATH' ],secure_filename (pname))
            pic_path=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(pname) )
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pname)))
            profile_img = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])

            with open(pic_path, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())


            profile_img.write({
                'profile_photo': my_string,

            })

        return http.request.render('gvp_website.save_page')

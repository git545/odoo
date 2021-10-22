import werkzeug
from odoo import http
import psycopg2
class Homepage(http.Controller):

    @http.route([ '/homepage' ], type='http', auth="user", website=True)
    def user_profiles_data(self, context=None, **kwargs):
        uid = str(http.request.session.uid)
        basic_prof_home = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.sidemenu_gvp',
                                   {'basic_prof_p': basic_prof_home,
                                    })

    @http.route('/myprofile', type='http', auth="user", website=True)
    def myprofile_page(self, **kwargs):

        uid = str(http.request.session.uid)
        partner = http.request.env.user.partner_id
        basic_prof_p = http.request.env[ 'tbl_basicinfo' ].search([ ('userid', '=', uid) ])
        user_prof_p = http.request.env[ 'res.partner' ].search([ ('id', '=', partner.id) ])
        edu_prof_p = http.request.env[ 'tbl_education' ].search([ ('userid', '=', uid) ])
        work_prof_p = http.request.env[ 'tbl_exp' ].search([ ('userid', '=', uid) ])
        cur_prof_p = http.request.env[ 'tbl_work' ].search([ ('userid', '=', uid) ])
        return http.request.render('gvp_website.myprof',
                                   {'users_profile_p': user_prof_p,
                                    'edu_profile_p': edu_prof_p,
                                    'basic_prof_p': basic_prof_p,
                                    'work_profile_p': work_prof_p,
                                    'current_profile_p': cur_prof_p,
                                    })

# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import http
from serial import tools
class Teachers(models.Model):
    _name = 'academy.teachers'
    name = fields.Char()
    biography = fields.Html()
    course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")
class Courses(models.Model):
    _name = 'academy.courses'
    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")
class userProfile(models.Model):
    #_name = 'partner_profile'
    _inherit = "res.partner"

    #mobile=fields.Char(string='aadhar No')
    channel_ids = fields.Many2many('mail.channel', 'mail_channel_profile_partner', 'partner_id', 'channel_id',
    copy=False)

class get_adm_year(models.Model):
    _name = 'tbl_year'
    _description = 'Admission/pass out year'
    start_year=fields.Char();
    pass_year=fields.Char();

    class Personal_details(models.Model):
        _name = 'tbl_basicinfo'
        _description = "Basic Information"
        edu_id = fields.One2many('tbl_education', 'bparent_id', string="Education Details")
        exp_id = fields.One2many('tbl_exp', 'bparent_id', string="Professional Experience")
        work_id = fields.One2many('tbl_work', 'bparent_id', string="Current Work Profile")
        fname = fields.Char(string="First name")
        lname = fields.Char(string="Last name")
        gender = fields.Selection([ ('Male', 'Male'), ('Female', 'female') ], string="Gender")
        dob = fields.Char(string="Date of Birth")
        pemail = fields.Char(string="Personal EmailID")
        aemail = fields.Char(string="Alternate EmailID")
        mobile = fields.Char(string="Mobile no")
        #profile_photo = fields.Binary(string="Profile Photo")
       # image = fields.Binary(string='Image',attachment=True)
        profile_photo = fields.Char(string="Profile Photo")
        addr = fields.Char(string="Address")
        city = fields.Char(string="City")
        pincode = fields.Char(string="Pincode")
        statename = fields.Char(string="State")
        countryname = fields.Char(string="Country")
        userid = fields.Integer(string="Userid")

    class USER_EDUCATION(models.Model):
        _name = 'tbl_education'
        _description = 'Education Details'

        instname = fields.Char(string="Institute Name")
        uniname = fields.Char(string="University Name")
        course = fields.Char(string='Course')
        fmonth = fields.Char(string='From Month')
        fyear = fields.Char(string='From Year')
        tmonth = fields.Char(string='To Month')
        tyear = fields.Char(string='To Year')
        chkstudy = fields.Boolean(string='checkstudy')
        bparent_id = fields.Many2one('tbl_basicinfo', string="Info")
        userid = fields.Integer(string="Userid")

class Professional_exp(models.Model):
    _name='tbl_exp'
    _description='Professional Experiance'
    bparent_id = fields.Many2one('tbl_basicinfo', string="Professional_info")
    orgname=fields.Char(string="Organization name")
    desg=fields.Char(string="Designation name")
    loc=fields.Char(string="Location")
    fmonth=fields.Char(string='From Month')
    fyear = fields.Char(string='From Year')
    tmonth = fields.Char(string='To Month')
    tyear = fields.Char(string='To Year')
    chkwork = fields.Boolean(string='checkwork')
    userid=fields.Integer(string="Userid")
class Work_profile(models.Model):
    _name='tbl_work'
    _description='Work Profile'
    bparent_id = fields.Many2one('tbl_basicinfo', string="Info")
    farea=fields.Char(string="Functional name")
    skills=fields.Char(string="Skill")
    rexp=fields.Char(string="Relevant Experience")
    industry=fields.Char(string='Industry')
    userid=fields.Integer(string="Userid")
class university_search(models.Model):
    _name='tbl_uni_name'
    _description='University Name List'
    uniname=fields.Char(string="University name")
class course_search(models.Model):
    _name='tbl_course'
    _description='Course Name List'
    cname=fields.Char(string="Course name")

class functionalarea_search(models.Model):
        _name = 'tbl_functional_area'
        _description = 'Functional Area List'
        funname = fields.Char(string="Functional Area name")

class Industry_search(models.Model):
        _name = 'tbl_industry'
        _description = 'Industry Area List'
        iname = fields.Char(string="Industry Area name")

class CountryList(models.Model):
    _name = 'tbl_country'
    _description = 'Country Name List'
    countryname = fields.Char(string="Country name")

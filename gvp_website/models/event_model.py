from odoo import models, fields, api
class Event_model(models.Model):
    _name = 'tbl_event'
    _description = 'Event table'
    event_title = fields.Char(string="Event Title")
    event_startdate = fields.Char(string="Event startdate")
    event_enddate = fields.Char(string="Event enddate")
    event_time = fields.Char(string="Event Time")
    event_desc = fields.Char(string="Event desc")
    event_url = fields.Char(string="Event URL")
    event_img = fields.Char(string="Event img")
    userid = fields.Integer(string="Userid")
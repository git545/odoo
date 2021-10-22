from odoo import models, fields, api


class Memories_model(models.Model):
    _name = 'tbl_memories'
    _description = 'Album table'
    mem_id = fields.One2many('tbl_album', 'mem_id', string="MemoriesID")
    album_name = fields.Char(string="Album Name")
    album_month = fields.Char(string="Album Month")
    album_year = fields.Char(string="Album Year")
    album_img = fields.Char(string="Album Photo")
    cnt=fields.Char(string="Count of Photo")
    userid = fields.Integer(string="Userid")
class Memories_allImages(models.Model):
    _name = 'tbl_album'
    _description = 'Album Images'
    mem_id = fields.Many2one('tbl_memories', string="Info")
    album_photo = fields.Char(string="Album Photo")
    album_desc = fields.Char(string="Description Album")
    userid = fields.Integer(string="Userid")



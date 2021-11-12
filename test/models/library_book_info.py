
from odoo import models, fields

class Books(models.Model):
	_name = 'books.lib'
	_description = 'Books'
	_sql_constraints = [('isbn_unique', 'unique(isbn)', 'Duplicate isbn not allowed')]


	name = fields.Char()
	price = fields.Float()
	# author_ids = fields.One2many('author', 'book_id')
	author_ids = fields.Many2many('author.lib')
	isbn = fields.Integer()
	category_id = fields.Many2one('book.category.lib')
	department_id = fields.Many2one('book.department.lib')
	barcode = fields.Char()
	publisher_id = fields.Many2one('book.publisher.lib')
	edition = fields.Char() # Many 2 one 
	date = fields.Date()
	shelf_id = fields.Many2one('shelf.lib')

class Author(models.Model):
	_name = 'author.lib'
	_description = 'Author'

	name = fields.Char()
	address = fields.Text()
	# book_id = fields.Many2one('books')

class BookCategory(models.Model):
	_name = 'book.category.lib'
	_description = 'Book Category'

	name = fields.Char()

class BookDepartment(models.Model):
	_name = 'book.department.lib'
	_description = 'Book Department'

	name = fields.Char()

class BookPublisher(models.Model):
	_name = 'book.publisher.lib'
	_description = 'Book Publisher'

	name = fields.Char()


class Rack(models.Model):
	_name = 'rack.lib'
	_description = 'Rack'

	name = fields.Char()
	sheld_ids = fields.One2many('rack.lib', 'rack_id')

class Shelf(models.Model):
	_name = 'shelf.lib'
	_description = 'Shelf'

	name = fields.Char()
	rack_id = fields.Many2one('rack.lib')



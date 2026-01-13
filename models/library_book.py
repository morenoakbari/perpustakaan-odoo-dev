from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'
    
    # Field wajib
    name = fields.Char(string='Judul Buku', required=True)
    author = fields.Char(string='Penulis')
    isbn = fields.Char(string='ISBN')
    tahun_terbit = fields.Integer(string='Tahun Terbit')
    
    # Field tambahan
    status = fields.Selection([
        ('tersedia', 'Tersedia'),
        ('dipinjam', 'Dipinjam'),
        ('rusak', 'Rusak'),
    ], string='Status', default='tersedia')
    
    jumlah_halaman = fields.Integer(string='Jumlah Halaman')
    sinopsis = fields.Text(string='Sinopsis')
    
    # Field sistem
    active = fields.Boolean(string='Active', default=True)
from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'
    _rec_name = 'name'

    name = fields.Char(
        string='Judul Buku',
        required=True
    )
    author = fields.Char(string='Penulis')
    isbn = fields.Char(string='ISBN')
    tahun_terbit = fields.Integer(string='Tahun Terbit')

    status = fields.Selection(
        [
            ('tersedia', 'Tersedia'),
            ('dipinjam', 'Dipinjam'),
            ('rusak', 'Rusak'),
        ],
        string='Status',
        default='tersedia'
    )

    jumlah_halaman = fields.Integer(string='Jumlah Halaman')
    sinopsis = fields.Text(string='Sinopsis')

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN harus unik!')
    ]

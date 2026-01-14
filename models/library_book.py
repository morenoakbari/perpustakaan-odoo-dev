from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'
    _rec_name = 'name'

    name = fields.Char(string='Judul Buku', required=True)
    author = fields.Char(string='Penulis')
    isbn = fields.Char(string='ISBN')

    tahun_terbit = fields.Char(
        string='Tahun Terbit',
        size=4
    )

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

    @api.constrains('tahun_terbit')
    def _check_tahun_terbit(self):
        for rec in self:
            if rec.tahun_terbit and (
                not rec.tahun_terbit.isdigit() or len(rec.tahun_terbit) != 4
            ):
                raise ValidationError(
                    "Tahun terbit harus 4 digit angka (contoh: 2025)"
                )

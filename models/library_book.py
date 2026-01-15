from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'
    _rec_name = 'name'

    # =====================
    # BASIC INFO
    # =====================
    name = fields.Char(
        string='Judul Buku',
        required=True
    )

    author = fields.Char(
        string='Penulis'
    )

    isbn = fields.Char(
        string='ISBN'
    )

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

    jumlah_halaman = fields.Integer(
        string='Jumlah Halaman'
    )

    sinopsis = fields.Text(
        string='Sinopsis'
    )

    active = fields.Boolean(
        default=True
    )

    # =====================
    # RELATION
    # =====================
    loan_ids = fields.One2many(
        'library.loan',
        'book_id',
        string='Riwayat Peminjaman'
    )

    # =====================
    # SQL CONSTRAINT
    # =====================
    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN harus unik!')
    ]

    # =====================
    # VALIDATION
    # =====================
    @api.constrains('tahun_terbit')
    def _check_tahun_terbit(self):
        for record in self:
            if record.tahun_terbit:
                if not record.tahun_terbit.isdigit() or len(record.tahun_terbit) != 4:
                    raise ValidationError(
                        "Tahun terbit harus 4 digit angka (contoh: 2025)"
                    )

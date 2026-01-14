from odoo import models, fields
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Peminjaman Buku'

    name = fields.Char(
        string='Nomor Peminjaman',
        default='New',
        readonly=True
    )

    book_id = fields.Many2one(
        'library.book',
        string='Buku',
        required=True
    )

    borrower_name = fields.Char(
        string='Nama Peminjam',
        required=True
    )

    borrow_date = fields.Date(
        string='Tanggal Pinjam',
        default=fields.Date.today
    )

    return_date = fields.Date(string='Tanggal Kembali')

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('borrowed', 'Dipinjam'),
            ('returned', 'Dikembalikan'),
        ],
        default='draft'
    )

    # 🔥 INI YANG KURANG
    def action_confirm_borrow(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError('Peminjaman sudah dikonfirmasi.')
            record.state = 'borrowed'

    def action_return_book(self):
        for record in self:
            if record.state != 'borrowed':
                raise ValidationError('Buku belum dipinjam.')
            record.state = 'returned'

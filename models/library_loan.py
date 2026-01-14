from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Peminjaman Buku'
    _order = 'borrow_date desc'

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

    return_date = fields.Date(
        string='Tanggal Kembali'
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('borrowed', 'Dipinjam'),
            ('returned', 'Dikembalikan'),
        ],
        default='draft'
    )

    # ===============================
    # ACTION BUTTON (ODOO 18 FRIENDLY)
    # ===============================

    def action_confirm_borrow(self):
        for record in self:
            if record.book_id.status != 'tersedia':
                raise ValidationError('Buku tidak tersedia untuk dipinjam.')

            record.state = 'borrowed'
            record.book_id.status = 'dipinjam'

    def action_return_book(self):
        for record in self:
            record.state = 'returned'
            if not record.return_date:
                record.return_date = fields.Date.today()
            record.book_id.status = 'tersedia'


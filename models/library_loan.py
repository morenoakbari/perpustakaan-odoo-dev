from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Peminjaman Buku'
    _order = 'borrow_date desc'

    # ===============================
    # FIELDS
    # ===============================

    name = fields.Char(
        string='Nomor Peminjaman',
        default='New',
        readonly=True,
        copy=False
    )

    book_id = fields.Many2one(
        'library.book',
        string='Buku',
        required=True,
        domain="[('status', '=', 'tersedia')]"
    )

    borrower_name = fields.Char(
        string='Nama Peminjam',
        required=True
    )

    borrow_date = fields.Date(
        string='Tanggal Pinjam',
        default=fields.Date.today,
        required=True
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
        string='Status',
        default='draft',
        tracking=True
    )

    # ===============================
    # CREATE (SEQUENCE)
    # ===============================

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'library.loan'
            ) or 'New'
        return super().create(vals)

    # ===============================
    # VALIDATIONS
    # ===============================

    @api.constrains('borrow_date', 'return_date')
    def _check_return_date(self):
        for record in self:
            if record.return_date and record.return_date < record.borrow_date:
                raise ValidationError(
                    'Tanggal kembali tidak boleh lebih awal dari tanggal pinjam.'
                )

    @api.constrains('book_id', 'state')
    def _check_book_availability(self):
        for record in self:
            if record.state == 'borrowed':
                loan = self.search([
                    ('book_id', '=', record.book_id.id),
                    ('state', '=', 'borrowed'),
                    ('id', '!=', record.id)
                ], limit=1)

                if loan:
                    raise ValidationError(
                        'Buku ini sedang dipinjam oleh peminjam lain.'
                    )

    # ===============================
    # BUTTON ACTIONS
    # ===============================

    def action_confirm_borrow(self):
        for record in self:
            if record.book_id.status != 'tersedia':
                raise ValidationError(
                    'Buku tidak tersedia untuk dipinjam.'
                )

            record.state = 'borrowed'
            record.book_id.status = 'dipinjam'

    def action_return_book(self):
        for record in self:
            record.state = 'returned'

            if not record.return_date:
                record.return_date = fields.Date.today()

            record.book_id.status = 'tersedia'

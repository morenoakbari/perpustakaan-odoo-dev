from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Peminjaman Buku'
    _order = 'borrow_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Nomor Peminjaman',
        default='New',
        readonly=True,
        copy=False
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
        default=fields.Date.today,
        required=True,
        readonly=True,
        copy=False
    )

    return_date = fields.Date(
        string='Tanggal Kembali'
    )

    late_days = fields.Integer(
        string='Hari Terlambat',
        compute='_compute_late_days'
    )

    fine_amount = fields.Integer(
        string='Denda (Rp)',
        compute='_compute_fine_amount'
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('borrowed', 'Dipinjam'),
            ('returned', 'Dikembalikan'),
        ],
        string='Status',
        default='draft'
    )

    # ===============================
    # SEQUENCE
    # ===============================
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'library.loan'
            ) or 'New'
        return super().create(vals)

    # ===============================
    # VALIDASI TANGGAL
    # ===============================
    @api.constrains('borrow_date', 'return_date')
    def _check_return_date(self):
        for rec in self:
            if rec.return_date and rec.return_date < rec.borrow_date:
                raise ValidationError(
                    'Borrow Date tidak boleh lebih kecil dari tanggal pinjam!'
                )

    # ===============================
    # HITUNG HARI TERLAMBAT
    # ===============================
    @api.depends('borrow_date', 'return_date')
    def _compute_late_days(self):
        max_days = 7
        for rec in self:
            rec.late_days = 0
            if rec.return_date:
                due_date = rec.borrow_date + timedelta(days=max_days)
                if rec.return_date > due_date:
                    rec.late_days = (rec.return_date - due_date).days

    # ===============================
    # HITUNG DENDA
    # ===============================
    @api.depends('late_days')
    def _compute_fine_amount(self):
        fine_per_day = 1000
        for rec in self:
            rec.fine_amount = rec.late_days * fine_per_day

    # ===============================
    # ACTION BUTTON
    # ===============================
    def action_confirm_borrow(self):
        for rec in self:
            if rec.book_id.status != 'tersedia':
                raise ValidationError('Buku tidak tersedia untuk dipinjam.')

            rec.borrow_date = fields.Date.today()
            
            rec.state = 'borrowed'
            rec.book_id.status = 'dipinjam'

    def action_return_book(self):
        for rec in self:
            rec.state = 'returned'
            if not rec.return_date:
                rec.return_date = fields.Date.today()
            rec.book_id.status = 'tersedia'
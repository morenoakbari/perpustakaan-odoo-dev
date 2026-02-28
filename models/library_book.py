from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'
    _rec_name = 'name'

    # =====================
    # BASIC INFO
    # =====================
    name = fields.Char(string='Judul Buku', required=True)

    image_cover = fields.Image(
        string='Cover Buku',
        max_width=1024,
        max_height=1024,
        help='Upload cover buku dengan ukuran maksimal 1024x1024 piksel'
    )

    image_cover_thumbnail = fields.Image(
        string='Thumbnail Cover',
        related='image_cover',
        max_width=256,
        max_height=256,
        store=True,
        help='Thumbnail otomatis dari cover buku'
    )

    author = fields.Char(string='Penulis')
    isbn = fields.Char(string='ISBN')

    tahun_terbit = fields.Char(string='Tahun Terbit', size=4)

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

    # =====================
    # EXPORT TO EXCEL
    # =====================
    def action_export_to_excel(self):
        for rec in self:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            sheet = workbook.add_worksheet('Riwayat Peminjaman')

            headers = [
                'Nomor Peminjaman',
                'Nama Peminjam',
                'Tanggal Pinjam',
                'Tanggal Kembali',
                'Status'
            ]

            for col, header in enumerate(headers):
                sheet.write(0, col, header)

            row = 1
            for loan in rec.loan_ids:
                sheet.write(row, 0, loan.name)
                sheet.write(row, 1, loan.borrower_name)
                sheet.write(row, 2, str(loan.borrow_date or ''))
                sheet.write(row, 3, str(loan.return_date or ''))
                sheet.write(row, 4, loan.state)
                row += 1

            workbook.close()
            output.seek(0)

            file_data = base64.b64encode(output.read())

            attachment = self.env['ir.attachment'].create({
                'name': f'Riwayat_{rec.name}.xlsx',
                'type': 'binary',
                'datas': file_data,
                'res_model': self._name,
                'res_id': rec.id,
            })

            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }
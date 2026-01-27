{
    'name': 'Sistem Perpustakaan',
    'version': '1.0',
    'summary': 'Modul untuk mengelola perpustakaan',
    'description': 'Modul sederhana untuk mengelola data buku dan peminjaman perpustakaan',
    'category': 'Services/Library',
    'author': 'Moreno',
    'depends': ['base', 'web'],   # web penting untuk assets
    'data': [
        'security/library_groups.xml',
        'security/ir.model.access.csv',
        'data/library_loan_sequence.xml',
        'views/library_book_views.xml',
        'views/library_loan_views.xml',
        'views/library_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library_management/static/src/scss/library_backend.scss',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

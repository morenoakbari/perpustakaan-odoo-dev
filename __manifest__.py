{
    'name': 'Sistem Perpustakaan',
    'version': '1.0',
    'summary': 'Modul untuk mengelola perpustakaan',
    'description': 'Modul sederhana untuk mengelola data buku perpustakaan',
    'category': 'Services/Library',
    'author': 'Nama Anda',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_menu_views.xml',
        'views/library_book_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
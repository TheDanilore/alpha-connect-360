{
    'name': 'Alpha Connect 360 - Navbar Theme',
    'version': '18.0.1.0.0',
    'category': 'Theme/Backend',
    'summary': 'Alpha Connect 360 customized navigation bar and interface',
    'description': """
Alpha Connect 360 Navbar Customization
=====================================
- Custom Alpha Connect 360 branded navbar
- Modified color scheme with Alpha Connect 360 colors
- Hidden Enterprise applications that require upgrade
- Modern interface design
    """,
    'author': 'Alpha Connect 360',
    'website': 'https://alphaconnect360.com',
    'depends': ['web', 'base'],
    'data': [
        'views/navbar_templates.xml',
        'views/app_filter_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'alpha_connect_navbar/static/src/scss/alpha_navbar.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

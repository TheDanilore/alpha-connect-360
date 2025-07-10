{
    'name': 'Alpha Connect - Tema y Personalización Completa',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Personalización completa del sistema Alpha Connect 360',
    'description': '''
        Personalización completa de Odoo para Alpha Connect:
        
        🎨 INTERFAZ PERSONALIZADA:
        - Logos y branding Alpha Connect
        - Colores corporativos personalizados
        - Iconografía y tipografía personalizada
        
        🔗 RUTAS PERSONALIZADAS:
        - Eliminar referencias a "Odoo" en URLs
        - Rutas limpias y amigables
        - Redirecciones optimizadas
        
        🔒 AUTENTICACIÓN PERSONALIZADA:
        - Login page personalizada
        - Gestor de base de datos personalizado
        - Mensajes de sistema personalizados
        
        📱 RESPONSIVIDAD:
        - Diseño mobile-first
        - Dashboard interactivo
        - UX optimizada para Alpha Connect
    ''',
    'author': 'Alpha Connect Development Team',
    'website': 'https://alphaconnect.com',
    'depends': [
        'base',
        'web',
        'crm',
        'mail',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/system_config.xml',
        'views/auth_signup_login_templates.xml',
        'views/web_templates.xml',
        'views/database_manager_templates.xml',
        'views/portal_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'alpha_connect_theme/static/src/css/alpha_variables.css',
            'alpha_connect_theme/static/src/css/alpha_backend.css',
            'alpha_connect_theme/static/src/css/alpha_login.css',
            'alpha_connect_theme/static/src/js/alpha_backend.js',
            'alpha_connect_theme/static/src/js/global_url_fixer.js',
        ],
        'web.assets_frontend': [
            'alpha_connect_theme/static/src/css/alpha_variables.css',
            'alpha_connect_theme/static/src/css/alpha_frontend.css',
            'alpha_connect_theme/static/src/js/alpha_frontend.js',
            'alpha_connect_theme/static/src/js/global_url_fixer.js',
        ],
        'web.assets_common': [
            'alpha_connect_theme/static/src/css/alpha_variables.css',
            'alpha_connect_theme/static/src/css/alpha_common.css',
            'alpha_connect_theme/static/src/js/global_url_fixer.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'sequence': 1,
}

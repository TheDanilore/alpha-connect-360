{
    'name': 'Alpha Connect - Core CRM',
    'version': '18.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Módulo principal CRM personalizado para Alpha Connect 360',
    'description': '''
        Módulo principal que extiende y personaliza el CRM de Odoo para Alpha Connect.
        Incluye:
        - Gestión avanzada de leads y oportunidades
        - Modelos de scoring predictivo
        - Integración con campañas automáticas
        - Extensiones de contactos y empresas
        - Flujos de conversión optimizados
    ''',
    'author': 'Alpha Connect',
    'website': 'https://alphaconnect.com',
    'depends': [
        'base',
        'crm',
        'sale',
        'mail',
        'contacts',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'data/crm_stage_data.xml',
        'data/crm_sequence_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'modulo_core_crm/static/src/css/crm_dashboard.css',
            'modulo_core_crm/static/src/js/crm_dashboard.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}

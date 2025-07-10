{
    'name': 'Alpha Connect - CRM Extension',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Extensiones personalizadas del CRM para Alpha Connect 360',
    'description': '''
        Extensiones del módulo CRM de Odoo para Alpha Connect:
        
        🤖 INTEGRACIÓN CON IA:
        - Campos de scoring predictivo de leads
        - Segmentación inteligente de clientes
        - Campos para datos de IA y machine learning
        
        📊 CAMPOS EXTENDIDOS:
        - Canal de adquisición detallado
        - Industria y tamaño de empresa
        - Scoring de conversión automático
        - Segmento de cliente calculado
        
        🔄 AUTOMATIZACIÓN:
        - Reglas de asignación automática
        - Workflows de seguimiento personalizado
        - Triggers para campañas automáticas
        
        📈 ANALYTICS AVANZADOS:
        - KPIs personalizados de Alpha Connect
        - Dashboard interactivo con métricas IA
        - Reportes de rendimiento predictivo
    ''',
    'author': 'Alpha Connect Development Team',
    'website': 'https://alphaconnect.com',
    'depends': [
        'crm',
        'sale',
        'mail',
        'alpha_connect_theme',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/lead_stages.xml',
        'data/acquisition_channels.xml',
        'data/industry_categories.xml',
        'views/crm_lead_views.xml',
        'views/res_partner_views.xml',
        'views/crm_stage_views.xml',
        'views/crm_dashboard_views.xml',
        'report/crm_reports.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'alpha_crm_extension/static/src/css/crm_dashboard.css',
            'alpha_crm_extension/static/src/js/crm_analytics.js',
        ],
    },
    'demo': [
        'demo/crm_demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}

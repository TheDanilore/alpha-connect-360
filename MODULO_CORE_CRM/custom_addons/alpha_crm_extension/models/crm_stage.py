# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    # Campos adicionales para las etapas del CRM
    stage_color = fields.Char(
        string='Stage Color',
        help='Color hexadecimal para la etapa (#RRGGBB)',
        default='#1f77b4'
    )
    
    conversion_probability = fields.Float(
        string='Default Conversion Probability',
        help='Probabilidad por defecto para leads en esta etapa',
        digits=(5, 2),
        default=0.0
    )
    
    expected_duration_days = fields.Integer(
        string='Expected Duration (Days)',
        help='Duración esperada en esta etapa en días',
        default=7
    )
    
    is_initial_stage = fields.Boolean(
        string='Is Initial Stage',
        help='Marcar si esta es la etapa inicial para nuevos leads',
        default=False
    )
    
    is_final_stage = fields.Boolean(
        string='Is Final Stage', 
        help='Marcar si esta es una etapa final (ganado/perdido)',
        default=False
    )
    
    requires_approval = fields.Boolean(
        string='Requires Approval',
        help='Requiere aprobación para mover leads a esta etapa',
        default=False
    )
    
    approval_user_ids = fields.Many2many(
        'res.users',
        string='Approval Users',
        help='Usuarios que pueden aprobar el movimiento a esta etapa'
    )
    
    automated_actions = fields.Text(
        string='Automated Actions',
        help='Acciones que se ejecutan automáticamente al llegar a esta etapa'
    )
    
    stage_description = fields.Text(
        string='Stage Description',
        help='Descripción detallada de qué se hace en esta etapa'
    )

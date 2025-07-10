# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Campos de scoring y analítica
    alpha_score = fields.Float(
        string='Alpha Score',
        default=0.0,
        help='Puntuación predictiva calculada por el sistema de IA'
    )
    
    alpha_score_reason = fields.Text(
        string='Razón del Score',
        help='Explicación de por qué se asignó este score'
    )
    
    # Campos de segmentación
    industry_segment = fields.Selection([
        ('technology', 'Tecnología'),
        ('finance', 'Finanzas'),
        ('healthcare', 'Salud'),
        ('education', 'Educación'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufactura'),
        ('services', 'Servicios'),
        ('other', 'Otro')
    ], string='Segmento de Industria')
    
    company_size = fields.Selection([
        ('startup', 'Startup (1-10)'),
        ('small', 'Pequeña (11-50)'),
        ('medium', 'Mediana (51-200)'),
        ('large', 'Grande (201-1000)'),
        ('enterprise', 'Empresa (1000+)')
    ], string='Tamaño de Empresa')
    
    # Campos de origen y campaña
    alpha_campaign_id = fields.Many2one(
        'alpha.campaign',
        string='Campaña Origen',
        help='Campaña que generó este lead'
    )
    
    alpha_source_detail = fields.Char(
        string='Detalle de Origen',
        help='Información adicional sobre el origen del lead'
    )
    
    # Campos de comportamiento
    website_visits = fields.Integer(
        string='Visitas al Sitio Web',
        default=0
    )
    
    email_opens = fields.Integer(
        string='Aperturas de Email',
        default=0
    )
    
    email_clicks = fields.Integer(
        string='Clicks en Email',
        default=0
    )
    
    social_engagement = fields.Float(
        string='Engagement Social',
        default=0.0,
        help='Nivel de engagement en redes sociales'
    )
    
    # Campos de tiempo
    first_contact_date = fields.Datetime(
        string='Primer Contacto',
        help='Fecha del primer contacto con el lead'
    )
    
    last_activity_date = fields.Datetime(
        string='Última Actividad',
        help='Fecha de la última actividad registrada'
    )
    
    response_time = fields.Float(
        string='Tiempo de Respuesta (horas)',
        help='Tiempo promedio de respuesta del lead'
    )
    
    # Campos de calificación manual
    budget_range = fields.Selection([
        ('low', 'Bajo (< $10K)'),
        ('medium', 'Medio ($10K - $50K)'),
        ('high', 'Alto ($50K - $100K)'),
        ('premium', 'Premium (> $100K)')
    ], string='Rango de Presupuesto')
    
    decision_timeline = fields.Selection([
        ('immediate', 'Inmediato (< 1 mes)'),
        ('short', 'Corto plazo (1-3 meses)'),
        ('medium', 'Mediano plazo (3-6 meses)'),
        ('long', 'Largo plazo (> 6 meses)')
    ], string='Timeline de Decisión')
    
    pain_points = fields.Text(
        string='Puntos de Dolor',
        help='Problemas principales que el lead quiere resolver'
    )
    
    @api.model
    def create(self, vals):
        """Override create para calcular score inicial"""
        lead = super(CrmLead, self).create(vals)
        lead._calculate_alpha_score()
        return lead
    
    def write(self, vals):
        """Override write para recalcular score cuando sea necesario"""
        result = super(CrmLead, self).write(vals)
        
        # Campos que disparan recálculo de score
        score_trigger_fields = [
            'industry_segment', 'company_size', 'website_visits',
            'email_opens', 'email_clicks', 'social_engagement',
            'budget_range', 'decision_timeline'
        ]
        
        if any(field in vals for field in score_trigger_fields):
            for lead in self:
                lead._calculate_alpha_score()
        
        return result
    
    def _calculate_alpha_score(self):
        """Calcula el Alpha Score basado en múltiples factores"""
        for lead in self:
            score = 0.0
            reasons = []
            
            # Score por segmento de industria (peso: 20%)
            industry_scores = {
                'technology': 25,
                'finance': 20,
                'healthcare': 18,
                'education': 15,
                'retail': 12,
                'manufacturing': 10,
                'services': 8,
                'other': 5
            }
            if lead.industry_segment:
                industry_score = industry_scores.get(lead.industry_segment, 0)
                score += industry_score
                reasons.append(f"Industria {lead.industry_segment}: +{industry_score}")
            
            # Score por tamaño de empresa (peso: 25%)
            size_scores = {
                'enterprise': 30,
                'large': 25,
                'medium': 20,
                'small': 15,
                'startup': 10
            }
            if lead.company_size:
                size_score = size_scores.get(lead.company_size, 0)
                score += size_score
                reasons.append(f"Tamaño {lead.company_size}: +{size_score}")
            
            # Score por presupuesto (peso: 25%)
            budget_scores = {
                'premium': 30,
                'high': 25,
                'medium': 15,
                'low': 5
            }
            if lead.budget_range:
                budget_score = budget_scores.get(lead.budget_range, 0)
                score += budget_score
                reasons.append(f"Presupuesto {lead.budget_range}: +{budget_score}")
            
            # Score por timeline (peso: 15%)
            timeline_scores = {
                'immediate': 20,
                'short': 15,
                'medium': 10,
                'long': 5
            }
            if lead.decision_timeline:
                timeline_score = timeline_scores.get(lead.decision_timeline, 0)
                score += timeline_score
                reasons.append(f"Timeline {lead.decision_timeline}: +{timeline_score}")
            
            # Score por engagement (peso: 15%)
            engagement_score = 0
            if lead.website_visits:
                engagement_score += min(lead.website_visits * 0.5, 5)
            if lead.email_opens:
                engagement_score += min(lead.email_opens * 0.3, 3)
            if lead.email_clicks:
                engagement_score += min(lead.email_clicks * 0.8, 4)
            if lead.social_engagement:
                engagement_score += min(lead.social_engagement * 0.2, 3)
            
            if engagement_score > 0:
                score += engagement_score
                reasons.append(f"Engagement digital: +{engagement_score:.1f}")
            
            # Actualizar campos
            lead.alpha_score = min(score, 100)  # Máximo 100
            lead.alpha_score_reason = "\n".join(reasons) if reasons else "Score no calculado - faltan datos"
            
            _logger.info(f"Lead {lead.id} - Score calculado: {lead.alpha_score}")
    
    def action_calculate_score(self):
        """Acción manual para recalcular score"""
        self._calculate_alpha_score()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f'Score recalculado: {self.alpha_score:.1f}',
                'type': 'success',
            }
        }
    
    @api.depends('alpha_score')
    def _compute_alpha_score_level(self):
        """Calcula el nivel de score para visualización"""
        for lead in self:
            if lead.alpha_score >= 80:
                lead.alpha_score_level = 'hot'
            elif lead.alpha_score >= 60:
                lead.alpha_score_level = 'warm'
            elif lead.alpha_score >= 40:
                lead.alpha_score_level = 'cold'
            else:
                lead.alpha_score_level = 'ice'
    
    alpha_score_level = fields.Selection([
        ('hot', 'Caliente (80+)'),
        ('warm', 'Tibio (60-79)'),
        ('cold', 'Frío (40-59)'),
        ('ice', 'Helado (<40)')
    ], string='Nivel de Score', compute='_compute_alpha_score_level', store=True)
    
    def action_convert_to_opportunity(self):
        """Override para agregar lógica adicional en conversión"""
        # Ejecutar conversión estándar
        result = super(CrmLead, self).action_convert_to_opportunity()
        
        # Lógica adicional para Alpha Connect
        for lead in self:
            if lead.type == 'opportunity':
                # Crear actividades automáticas basadas en el score
                if lead.alpha_score >= 80:
                    # Lead caliente - programar llamada inmediata
                    self.env['mail.activity'].create({
                        'res_id': lead.id,
                        'res_model': 'crm.lead',
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'summary': 'URGENTE: Lead de alto score - Contactar inmediatamente',
                        'date_deadline': fields.Date.today(),
                        'user_id': lead.user_id.id or self.env.user.id,
                    })
                elif lead.alpha_score >= 60:
                    # Lead tibio - programar seguimiento en 2 días
                    self.env['mail.activity'].create({
                        'res_id': lead.id,
                        'res_model': 'crm.lead',
                        'activity_type_id': self.env.ref('mail.mail_activity_data_email').id,
                        'summary': 'Lead prometedor - Enviar propuesta personalizada',
                        'date_deadline': fields.Date.add(fields.Date.today(), days=2),
                        'user_id': lead.user_id.id or self.env.user.id,
                    })
        
        return result

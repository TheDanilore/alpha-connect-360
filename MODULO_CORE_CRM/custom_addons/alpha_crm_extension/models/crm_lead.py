# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
import json

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Campos para integración con IA
    ai_conversion_score = fields.Float(
        string='AI Conversion Score',
        help='Probabilidad de conversión calculada por IA (0-100)',
        digits=(5, 2),
        default=0.0,
        index=True
    )
    
    ai_customer_segment = fields.Selection([
        ('high_value', 'High Value Prospect'),
        ('medium_value', 'Medium Value Prospect'), 
        ('low_value', 'Low Value Prospect'),
        ('hot_lead', 'Hot Lead'),
        ('warm_lead', 'Warm Lead'),
        ('cold_lead', 'Cold Lead'),
        ('enterprise', 'Enterprise'),
        ('sme', 'Small & Medium Enterprise'),
        ('startup', 'Startup'),
    ], string='AI Customer Segment', help='Segmento calculado por IA')
    
    ai_recommended_actions = fields.Text(
        string='AI Recommended Actions',
        help='Acciones recomendadas por la IA'
    )
    
    ai_last_analysis_date = fields.Datetime(
        string='Last AI Analysis',
        help='Última vez que la IA analizó este lead'
    )
    
    # Campos extendidos para mejor segmentación
    acquisition_channel = fields.Selection([
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('email_marketing', 'Email Marketing'),
        ('google_ads', 'Google Ads'),
        ('facebook_ads', 'Facebook Ads'),
        ('linkedin', 'LinkedIn'),
        ('referral', 'Referral'),
        ('trade_show', 'Trade Show'),
        ('cold_call', 'Cold Call'),
        ('direct_mail', 'Direct Mail'),
        ('partner', 'Partner'),
        ('other', 'Other'),
    ], string='Acquisition Channel', help='Canal por el que llegó el lead')
    
    industry_sector = fields.Selection([
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance & Banking'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('education', 'Education'),
        ('real_estate', 'Real Estate'),
        ('hospitality', 'Hospitality'),
        ('automotive', 'Automotive'),
        ('energy', 'Energy'),
        ('telecommunications', 'Telecommunications'),
        ('government', 'Government'),
        ('non_profit', 'Non-Profit'),
        ('other', 'Other'),
    ], string='Industry Sector')
    
    company_size = fields.Selection([
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-1000', '201-1000 employees'),
        ('1000+', '1000+ employees'),
    ], string='Company Size')
    
    annual_revenue_range = fields.Selection([
        ('0-100k', '$0 - $100K'),
        ('100k-500k', '$100K - $500K'),
        ('500k-1m', '$500K - $1M'),
        ('1m-5m', '$1M - $5M'),
        ('5m-10m', '$5M - $10M'),
        ('10m+', '$10M+'),
    ], string='Annual Revenue Range')
    
    # Campos de comportamiento y engagement
    website_sessions = fields.Integer(string='Website Sessions', default=0)
    email_opens = fields.Integer(string='Email Opens', default=0)
    email_clicks = fields.Integer(string='Email Clicks', default=0)
    social_engagement_score = fields.Float(string='Social Engagement Score', default=0.0)
    
    # Campos de timeline y urgencia
    urgency_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Urgency Level', default='medium')
    
    decision_timeline = fields.Selection([
        ('immediate', 'Immediate (0-30 days)'),
        ('short_term', 'Short Term (1-3 months)'),
        ('medium_term', 'Medium Term (3-6 months)'),
        ('long_term', 'Long Term (6+ months)'),
    ], string='Decision Timeline')
    
    # Campos de competencia
    competitor_analysis = fields.Text(string='Competitor Analysis')
    competitive_advantage = fields.Text(string='Our Competitive Advantage')
    
    # Campos calculados
    lead_quality_score = fields.Float(
        string='Lead Quality Score',
        compute='_compute_lead_quality_score',
        store=True,
        help='Score basado en múltiples factores (0-100)'
    )
    
    engagement_score = fields.Float(
        string='Engagement Score',
        compute='_compute_engagement_score',
        store=True,
        help='Score basado en interacciones (0-100)'
    )

    @api.depends('ai_conversion_score', 'probability', 'urgency_level', 'company_size', 'annual_revenue_range')
    def _compute_lead_quality_score(self):
        """Calcula el score de calidad del lead basado en múltiples factores"""
        for lead in self:
            score = 0.0
            
            # Base score from AI if available, otherwise use probability
            if lead.ai_conversion_score > 0:
                score += lead.ai_conversion_score * 0.4  # 40% weight
            else:
                score += lead.probability * 0.4
            
            # Urgency weight
            urgency_weights = {
                'critical': 30,
                'high': 20,
                'medium': 10,
                'low': 5
            }
            score += urgency_weights.get(lead.urgency_level, 0)
            
            # Company size weight
            size_weights = {
                '1000+': 20,
                '201-1000': 15,
                '51-200': 10,
                '11-50': 5,
                '1-10': 2
            }
            score += size_weights.get(lead.company_size, 0)
            
            # Revenue weight
            revenue_weights = {
                '10m+': 15,
                '5m-10m': 12,
                '1m-5m': 10,
                '500k-1m': 8,
                '100k-500k': 5,
                '0-100k': 2
            }
            score += revenue_weights.get(lead.annual_revenue_range, 0)
            
            lead.lead_quality_score = min(score, 100.0)  # Cap at 100

    @api.depends('website_sessions', 'email_opens', 'email_clicks', 'social_engagement_score')
    def _compute_engagement_score(self):
        """Calcula el score de engagement basado en interacciones"""
        for lead in self:
            score = 0.0
            
            # Website engagement (max 30 points)
            if lead.website_sessions > 0:
                score += min(lead.website_sessions * 3, 30)
            
            # Email engagement (max 40 points)
            if lead.email_opens > 0:
                score += min(lead.email_opens * 2, 20)
            if lead.email_clicks > 0:
                score += min(lead.email_clicks * 5, 20)
            
            # Social engagement (max 30 points)
            score += min(lead.social_engagement_score, 30)
            
            lead.engagement_score = min(score, 100.0)

    def action_request_ai_analysis(self):
        """Botón para solicitar análisis de IA del lead"""
        self.ensure_one()
        
        # Aquí se integrará con el microservicio de IA
        # Por ahora, simulamos el comportamiento
        
        self.ai_last_analysis_date = fields.Datetime.now()
        
        # Simulación de scoring (se reemplazará con llamada real a la IA)
        base_score = self.probability if self.probability else 50.0
        
        # Ajustes basados en datos disponibles
        if self.company_size in ['201-1000', '1000+']:
            base_score += 15
        if self.urgency_level in ['high', 'critical']:
            base_score += 10
        if self.engagement_score > 50:
            base_score += 10
            
        self.ai_conversion_score = min(base_score, 100.0)
        
        # Asignar segmento basado en score
        if self.ai_conversion_score >= 80:
            self.ai_customer_segment = 'hot_lead'
        elif self.ai_conversion_score >= 60:
            self.ai_customer_segment = 'warm_lead'
        else:
            self.ai_customer_segment = 'cold_lead'
            
        self.ai_recommended_actions = self._generate_ai_recommendations()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': _("AI analysis completed successfully!"),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def _generate_ai_recommendations(self):
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        if self.ai_conversion_score >= 80:
            recommendations.append("🔥 High conversion probability - Prioritize immediate follow-up")
            recommendations.append("📞 Schedule demo/meeting within 24 hours")
            
        elif self.ai_conversion_score >= 60:
            recommendations.append("⚡ Good conversion potential - Follow up within 2-3 days")
            recommendations.append("📧 Send personalized proposal")
            
        else:
            recommendations.append("📚 Nurture with educational content")
            recommendations.append("⏰ Schedule follow-up in 1-2 weeks")
            
        if self.engagement_score < 30:
            recommendations.append("📱 Increase engagement through social media")
            
        if not self.phone:
            recommendations.append("📞 Obtain phone number for better communication")
            
        return "\n".join(recommendations)

    @api.model
    def create(self, vals):
        """Override create to trigger AI analysis for new leads"""
        lead = super(CrmLead, self).create(vals)
        
        # Auto-trigger AI analysis for leads with sufficient data
        if lead.email and lead.company_size and lead.industry_sector:
            try:
                lead.action_request_ai_analysis()
            except Exception as e:
                _logger.warning(f"Failed to auto-trigger AI analysis for lead {lead.id}: {e}")
                
        return lead

    def write(self, vals):
        """Override write to update AI analysis when relevant fields change"""
        result = super(CrmLead, self).write(vals)
        
        # Trigger re-analysis if key fields changed
        trigger_fields = ['email', 'phone', 'company_size', 'industry_sector', 'annual_revenue_range', 'urgency_level']
        if any(field in vals for field in trigger_fields):
            for lead in self:
                if lead.ai_last_analysis_date:
                    try:
                        lead.action_request_ai_analysis()
                    except Exception as e:
                        _logger.warning(f"Failed to update AI analysis for lead {lead.id}: {e}")
                        
        return result

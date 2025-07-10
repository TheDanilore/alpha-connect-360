# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Campos para scoring y segmentación de clientes existentes
    customer_lifetime_value = fields.Float(
        string='Customer Lifetime Value (CLV)',
        help='Valor de vida del cliente calculado por IA',
        digits=(12, 2),
        default=0.0
    )
    
    churn_risk_score = fields.Float(
        string='Churn Risk Score',
        help='Probabilidad de abandono (0-100)',
        digits=(5, 2),
        default=0.0
    )
    
    satisfaction_score = fields.Float(
        string='Satisfaction Score',
        help='Score de satisfacción del cliente (1-10)',
        digits=(3, 1),
        default=0.0
    )
    
    # Segmentación avanzada
    customer_segment = fields.Selection([
        ('vip', 'VIP Customer'),
        ('loyal', 'Loyal Customer'),
        ('potential', 'Potential Customer'),
        ('at_risk', 'At Risk'),
        ('lost', 'Lost Customer'),
        ('new', 'New Customer'),
        ('champion', 'Champion'),
        ('promoter', 'Promoter'),
        ('detractor', 'Detractor'),
    ], string='Customer Segment')
    
    # Comportamiento de compra
    purchase_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('irregular', 'Irregular'),
    ], string='Purchase Frequency')
    
    avg_order_value = fields.Float(
        string='Average Order Value',
        compute='_compute_avg_order_value',
        store=True,
        digits=(12, 2)
    )
    
    total_orders = fields.Integer(
        string='Total Orders',
        compute='_compute_order_stats',
        store=True
    )
    
    last_order_date = fields.Date(
        string='Last Order Date',
        compute='_compute_order_stats',
        store=True
    )
    
    # Engagement y comunicación
    preferred_communication_channel = fields.Selection([
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('social_media', 'Social Media'),
        ('in_person', 'In Person'),
    ], string='Preferred Communication')
    
    communication_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('as_needed', 'As Needed'),
    ], string='Communication Frequency')
    
    # Información de la empresa (si es B2B)
    company_industry = fields.Selection([
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
    ], string='Company Industry')
    
    company_size_range = fields.Selection([
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
    ], string='Annual Revenue')
    
    # Campos de IA y análisis predictivo
    ai_recommendations = fields.Text(
        string='AI Recommendations',
        help='Recomendaciones personalizadas generadas por IA'
    )
    
    next_best_action = fields.Text(
        string='Next Best Action',
        help='Siguiente mejor acción recomendada por IA'
    )
    
    ai_last_update = fields.Datetime(
        string='AI Last Update',
        help='Última actualización de datos de IA'
    )
    
    # Loyalty program fields
    loyalty_points = fields.Integer(string='Loyalty Points', default=0)
    loyalty_tier = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    ], string='Loyalty Tier')
    
    # Social media presence
    linkedin_profile = fields.Char(string='LinkedIn Profile')
    twitter_handle = fields.Char(string='Twitter Handle')
    facebook_profile = fields.Char(string='Facebook Profile')
    instagram_handle = fields.Char(string='Instagram Handle')
    
    @api.depends('sale_order_ids', 'sale_order_ids.amount_total')
    def _compute_avg_order_value(self):
        """Calcula el valor promedio de pedidos"""
        for partner in self:
            orders = partner.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            if orders:
                partner.avg_order_value = sum(orders.mapped('amount_total')) / len(orders)
            else:
                partner.avg_order_value = 0.0

    @api.depends('sale_order_ids')
    def _compute_order_stats(self):
        """Calcula estadísticas de pedidos"""
        for partner in self:
            orders = partner.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            partner.total_orders = len(orders)
            partner.last_order_date = max(orders.mapped('date_order'), default=False)

    def action_analyze_customer_behavior(self):
        """Acción para analizar comportamiento del cliente con IA"""
        self.ensure_one()
        
        # Aquí se integrará con el microservicio de IA
        # Por ahora simulamos el comportamiento
        
        self.ai_last_update = fields.Datetime.now()
        
        # Simular cálculo de CLV
        if self.total_orders > 0 and self.avg_order_value > 0:
            # Formula simplificada: AOV * Frequency * Lifetime
            frequency_multipliers = {
                'daily': 365,
                'weekly': 52,
                'monthly': 12,
                'quarterly': 4,
                'yearly': 1,
                'irregular': 2
            }
            frequency = frequency_multipliers.get(self.purchase_frequency, 1)
            estimated_lifetime = 3  # 3 años promedio
            
            self.customer_lifetime_value = self.avg_order_value * frequency * estimated_lifetime
        
        # Simular score de riesgo de abandono
        days_since_last_order = 0
        if self.last_order_date:
            days_since_last_order = (fields.Date.today() - self.last_order_date).days
        
        if days_since_last_order > 365:
            self.churn_risk_score = 80.0
        elif days_since_last_order > 180:
            self.churn_risk_score = 50.0
        elif days_since_last_order > 90:
            self.churn_risk_score = 25.0
        else:
            self.churn_risk_score = 10.0
        
        # Asignar segmento basado en CLV y churn risk
        if self.customer_lifetime_value > 10000 and self.churn_risk_score < 20:
            self.customer_segment = 'vip'
        elif self.customer_lifetime_value > 5000 and self.churn_risk_score < 30:
            self.customer_segment = 'loyal'
        elif self.churn_risk_score > 70:
            self.customer_segment = 'at_risk'
        elif self.total_orders <= 2:
            self.customer_segment = 'new'
        else:
            self.customer_segment = 'potential'
        
        # Generar recomendaciones
        self.ai_recommendations = self._generate_customer_recommendations()
        self.next_best_action = self._generate_next_best_action()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': _("Customer behavior analysis completed!"),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def _generate_customer_recommendations(self):
        """Genera recomendaciones para el cliente"""
        recommendations = []
        
        if self.customer_segment == 'vip':
            recommendations.append("🌟 VIP Treatment: Assign dedicated account manager")
            recommendations.append("🎁 Offer exclusive products and early access")
            
        elif self.customer_segment == 'at_risk':
            recommendations.append("⚠️ Immediate retention campaign required")
            recommendations.append("📞 Personal call to understand concerns")
            recommendations.append("💰 Consider special discount or loyalty reward")
            
        elif self.customer_segment == 'new':
            recommendations.append("🎉 Welcome campaign with onboarding materials")
            recommendations.append("📚 Educational content about product usage")
            
        if self.churn_risk_score > 50:
            recommendations.append("🔔 Set up automated retention alerts")
            
        if self.avg_order_value > 0:
            recommendations.append(f"📈 Upsell opportunities based on ${self.avg_order_value:.0f} AOV")
            
        return "\n".join(recommendations)

    def _generate_next_best_action(self):
        """Genera la siguiente mejor acción"""
        if self.customer_segment == 'vip':
            return "Schedule quarterly business review meeting"
        elif self.customer_segment == 'at_risk':
            return "Immediate outreach - Risk of churn detected"
        elif self.customer_segment == 'new':
            return "Send welcome package and setup onboarding call"
        elif self.churn_risk_score > 70:
            return "Launch win-back campaign with special offer"
        else:
            return "Regular follow-up and cross-sell evaluation"

    @api.model
    def cron_update_customer_analytics(self):
        """Cron job para actualizar analytics de clientes automáticamente"""
        # Buscar customers que necesitan actualización (más de 30 días)
        cutoff_date = fields.Datetime.now() - timedelta(days=30)
        customers = self.search([
            ('is_company', '=', False),
            ('customer_rank', '>', 0),
            '|',
            ('ai_last_update', '<', cutoff_date),
            ('ai_last_update', '=', False)
        ], limit=100)  # Procesar máximo 100 por ejecución
        
        for customer in customers:
            try:
                customer.action_analyze_customer_behavior()
            except Exception as e:
                _logger.error(f"Error updating customer analytics for {customer.id}: {e}")
                
        _logger.info(f"Updated analytics for {len(customers)} customers")

# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from odoo.addons.web.controllers.main import Database
from odoo.addons.web.controllers.session import Session
import logging
import werkzeug
import re

_logger = logging.getLogger(__name__)


class AlphaConnectSession(Session):
    """
    Controlador personalizado para sesiones Alpha Connect
    Sobreescribe el logout para evitar redirecciones a '/odoo'
    """
    
    @http.route('/web/session/logout', type='http', auth='none', readonly=True)
    def logout(self, redirect='/web'):
        """
        Sobrescribimos el método de cierre de sesión para redirigir a '/web' en lugar de '/odoo'
        """
        _logger.info("Alpha Connect: Cierre de sesión personalizado")
        request.session.logout(keep_db=True)
        return request.redirect(redirect, 303)


class AlphaConnectHome(Home):
    """
    Controlador personalizado para Alpha Connect
    Maneja las rutas principales y redirecciones
    """
    
    @http.route(['/odoo', '/odoo/<path:path>'], type='http', auth="none", sitemap=False)
    def odoo_redirect(self, path='', **kw):
        """
        Interceptor de rutas /odoo para redirigir a /web
        Esta es la función principal para capturar y corregir URLs incorrectas
        """
        _logger.info(f"Alpha Connect: Interceptando ruta /odoo/{path} con parámetros {kw}")
        
        # Casos específicos para el selector de base de datos
        if 'db' in kw:
            db_name = kw.get('db')
            if path == '' or not path:
                _logger.info(f"Alpha Connect: Redirigiendo a login con db={db_name}")
                return request.redirect(f'/web/login?db={db_name}')
        
        # Mapeo de rutas específicas
        path_mapping = {
            '': '/web',
            'apps': '/web/apps',
            'web': '/web',
        }
        
        redirect_path = path_mapping.get(path, f'/web/{path}')
        
        # Agregar parámetros query si existen
        if kw:
            # Excluir 'path' si está en kw
            query_params = {k: v for k, v in kw.items() if k != 'path'}
            if query_params:
                from werkzeug.urls import url_encode
                redirect_path += f"?{url_encode(query_params)}"
                
        _logger.info(f"Alpha Connect: Redirigiendo a {redirect_path}")
        return request.redirect(redirect_path, 301)  # 301 es redirección permanente

    @http.route('/', type='http', auth="none", sitemap=False)
    def web_client(self, s_action=None, **kw):
        """
        Ruta principal personalizada para Alpha Connect
        Elimina referencias a 'odoo' en las URLs
        """
        _logger.info("Alpha Connect: Acceso a ruta principal")
        
        # Si no hay base de datos, redirigir al selector
        if not request.session.db:
            return request.redirect('/web/database/selector')
        
        # Si hay base de datos pero no está logueado, ir al login
        if not request.session.uid:
            return request.redirect('/web/login')
        
        # Si está logueado, ir al dashboard principal
        return super(AlphaConnectHome, self).web_client(s_action, **kw)

    @http.route('/web', type='http', auth="none", website=True, sitemap=False)
    def web_index(self, s_action=None, **kw):
        """
        Ruta web personalizada para Alpha Connect
        Asegura que se mantenga sin 'odoo' en las URLs
        """
        _logger.info("Alpha Connect: Acceso a ruta /web")
        return super(AlphaConnectHome, self).web_client(s_action, **kw)

    @http.route('/apps', type='http', auth="user")
    def web_client_apps(self, **kw):
        """
        Ruta personalizada para Apps (sin /odoo/)
        """
        _logger.info("Alpha Connect: Acceso a /apps")
        return request.redirect('/web#action=base.open_module_tree')

    @http.route('/dashboard', type='http', auth="user")
    def web_client_dashboard(self, **kw):
        """
        Ruta personalizada para Dashboard
        """
        _logger.info("Alpha Connect: Acceso a /dashboard")
        return request.redirect('/web#action=board.open_board_my_dash_action')

    @http.route('/crm', type='http', auth="user")
    def web_client_crm(self, **kw):
        """
        Ruta directa al CRM
        """
        _logger.info("Alpha Connect: Acceso directo a CRM")
        return request.redirect('/web#action=crm.crm_lead_all_leads')

    @http.route('/leads', type='http', auth="user")
    def web_client_leads(self, **kw):
        """
        Ruta directa a Leads
        """
        _logger.info("Alpha Connect: Acceso directo a Leads")
        return request.redirect('/web#action=crm.crm_lead_action_pipeline')

    @http.route('/opportunities', type='http', auth="user")
    def web_client_opportunities(self, **kw):
        """
        Ruta directa a Oportunidades
        """
        _logger.info("Alpha Connect: Acceso directo a Oportunidades")
        return request.redirect('/web#action=crm.action_your_pipeline')

    @http.route('/contacts', type='http', auth="user")
    def web_client_contacts(self, **kw):
        """
        Ruta directa a Contactos
        """
        _logger.info("Alpha Connect: Acceso directo a Contactos")
        return request.redirect('/web#action=contacts.action_contacts')

    @http.route('/campaigns', type='http', auth="user")
    def web_client_campaigns(self, **kw):
        """
        Ruta directa a Campañas (microservicio Laravel)
        """
        _logger.info("Alpha Connect: Redirección a módulo de Campañas")
        # Redirigir directamente al microservicio Laravel
        return werkzeug.utils.redirect('http://localhost:8080/campaigns')

    @http.route('/integrations', type='http', auth="user")
    def web_client_integrations(self, **kw):
        """
        Ruta directa a Integraciones (microservicio Node.js)
        """
        _logger.info("Alpha Connect: Redirección a módulo de Integraciones")
        # Redirigir directamente al microservicio Node.js
        return werkzeug.utils.redirect('http://localhost:3000/integrations')

    @http.route('/ai-insights', type='http', auth="user")
    def web_client_ai_insights(self, **kw):
        """
        Ruta directa a IA Insights (microservicio Python)
        """
        _logger.info("Alpha Connect: Redirección a módulo de IA")
        # Redirigir directamente al microservicio Python/FastAPI
        return werkzeug.utils.redirect('http://localhost:8000/ai-insights')

    # Añadimos una ruta específica para /web
    @http.route('/web', type='http', auth="none", sitemap=False)
    def web_index(self, s_action=None, **kw):
        """
        Ruta /web personalizada para evitar redirecciones a /odoo
        """
        _logger.info("Alpha Connect: Acceso a ruta /web")
        
        # Si no hay base de datos, redirigir al selector
        if not request.session.db:
            return request.redirect('/web/database/selector')
        
        # Si hay base de datos pero no está logueado, ir al login
        if not request.session.uid:
            return request.redirect('/web/login')
        
        # Si está logueado, ir al dashboard principal
        return super(AlphaConnectHome, self).web_client(s_action, **kw)
    
    @http.route(['/odoo', '/odoo/', '/odoo/<path:path>'], type='http', auth="none")
    def redirect_odoo_paths(self, path='', **kw):
        """
        Redirigir todas las rutas que contengan /odoo/ a rutas limpias
        """
        _logger.info(f"Alpha Connect: Redirigiendo ruta /odoo/{path}")
        
        # Manejo especial para casos de base de datos
        if 'db' in kw:
            db_name = kw.get('db')
            # Si es la ruta de login con db
            if path == '' or not path:
                return request.redirect(f'/web/login?db={db_name}')
            elif path == 'apps':
                return request.redirect('/web#action=base.open_module_tree')
        
        # Mapeo de rutas /odoo/ a rutas limpias
        path_mapping = {
            '': '/web',
            'apps': '/apps',
            'dashboard': '/dashboard',
            'crm': '/crm',
            'leads': '/leads',
            'opportunities': '/opportunities',
            'contacts': '/contacts',
            'campaigns': '/campaigns',
            'integrations': '/integrations',
            'ai-insights': '/ai-insights',
        }
        
        # Si la ruta está mapeada, redirigir
        if path in path_mapping:
            redirect_url = path_mapping[path]
            # Preservar cualquier parámetro adicional en la URL
            query_params = {k: v for k, v in kw.items() if k != 'path'}
            if query_params:
                from werkzeug.urls import url_encode
                redirect_url = f"{redirect_url}?{url_encode(query_params)}"
            return request.redirect(redirect_url)
        
        # Si no está mapeada pero tiene acción, redirigir preservando la acción
        if '#' in path:
            base_path, action = path.split('#', 1)
            return request.redirect(f'/web#{action}')
        
        # Si no está mapeada, redirigir a la raíz
        return request.redirect('/web')


class AlphaConnectDatabase(Database):
    """
    Controlador personalizado para el gestor de base de datos
    """

    @http.route('/web/database/selector', type='http', auth="none")
    def selector(self, **kw):
        """
        Selector de base de datos personalizado
        """
        _logger.info("Alpha Connect: Acceso al selector de base de datos")
        return super(AlphaConnectDatabase, self).selector(**kw)

    @http.route('/web/database/manager', type='http', auth="none")
    def manager(self, **kw):
        """
        Gestor de base de datos personalizado
        """
        _logger.info("Alpha Connect: Acceso al gestor de base de datos")
        return super(AlphaConnectDatabase, self).manager(**kw)
        
    @http.route('/web/database/create', type='http', auth="none")
    def create(self, **post):
        """
        Creación de base de datos personalizada - corrige la redirección
        """
        _logger.info("Alpha Connect: Creando nueva base de datos")
        response = super(AlphaConnectDatabase, self).create(**post)
        
        # Si es una redirección, cambiar la URL de destino para quitar /odoo
        if hasattr(response, 'location') and '/odoo' in response.location:
            new_location = response.location.replace('/odoo', '/web')
            response.location = new_location
            _logger.info(f"Alpha Connect: Redirigiendo a {new_location}")
        
        return response
    
    @http.route('/web/database/duplicate', type='http', auth="none")
    def duplicate(self, **post):
        """
        Duplicación de base de datos personalizada - corrige la redirección
        """
        _logger.info("Alpha Connect: Duplicando base de datos")
        response = super(AlphaConnectDatabase, self).duplicate(**post)
        
        # Si es una redirección, cambiar la URL de destino para quitar /odoo
        if hasattr(response, 'location') and '/odoo' in response.location:
            new_location = response.location.replace('/odoo', '/web')
            response.location = new_location
            _logger.info(f"Alpha Connect: Redirigiendo a {new_location}")
        
        return response

    @http.route('/web/database/drop', type='http', auth="none")
    def drop(self, **post):
        """
        Eliminación de base de datos personalizada - corrige la redirección
        """
        _logger.info("Alpha Connect: Eliminando base de datos")
        response = super(AlphaConnectDatabase, self).drop(**post)
        
        # Si es una redirección, cambiar la URL de destino para quitar /odoo
        if hasattr(response, 'location') and '/odoo' in response.location:
            new_location = response.location.replace('/odoo', '/web')
            response.location = new_location
            _logger.info(f"Alpha Connect: Redirigiendo a {new_location}")
        
        return response

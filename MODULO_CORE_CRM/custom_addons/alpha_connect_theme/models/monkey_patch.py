# -*- coding: utf-8 -*-

import logging
from odoo import api, models, SUPERUSER_ID
from odoo.http import request, Response
import werkzeug
import re

_logger = logging.getLogger(__name__)

# Guardar la función original de redirect
original_redirect = werkzeug.utils.redirect

# Función para interceptar todas las redirecciones
def patched_redirect(location, code=302, Response=Response):
    """
    Intercepta todas las redirecciones y reemplaza '/odoo' por '/web'
    """
    if location and isinstance(location, str):
        # Expresión regular para detectar /odoo en diferentes posiciones
        odoo_pattern = r'(^/odoo($|/)|(\?|&)redirect=/odoo($|/))'
        
        if re.search(odoo_pattern, location):
            _logger.info(f"Alpha Connect: Interceptando redirección a {location}")
            
            # Caso especial: /odoo?db=nombre_db
            if location.startswith('/odoo?db='):
                db_name = location.split('db=')[1].split('&')[0]
                new_location = f'/web/login?db={db_name}'
            # Caso general: reemplazar /odoo por /web
            else:
                new_location = re.sub(r'/odoo($|/)', '/web\\1', location)
                # También reemplazar en parámetros de URL
                new_location = re.sub(r'(redirect=)/odoo($|/)', '\\1/web\\2', new_location)
            
            _logger.info(f"Alpha Connect: Redirigiendo a {new_location}")
            return original_redirect(new_location, code, Response)
        
    return original_redirect(location, code, Response)

# Reemplazar la función de redirección en werkzeug
werkzeug.utils.redirect = patched_redirect

class AlphaConnectMonkeyPatch(models.AbstractModel):
    _name = 'alpha.connect.monkey.patch'
    _description = 'Monkey Patches para Alpha Connect'
    
    def init(self):
        _logger.info("Alpha Connect: Aplicando monkey patches...")
        
        # Aquí podemos aplicar otros monkey patches si es necesario
        
        # Ejemplo: Modificar el título de la página
        from odoo.addons.web.controllers.main import Home
        original_web_client = Home.web_client
        
        def patched_web_client(self, s_action=None, **kw):
            response = original_web_client(self, s_action, **kw)
            if hasattr(response, 'qcontext'):
                response.qcontext['title'] = "Alpha Connect"
            return response
        
        Home.web_client = patched_web_client

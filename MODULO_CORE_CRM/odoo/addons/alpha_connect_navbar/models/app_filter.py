from odoo import models, api


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def get_apps_menu(self):
        """Override to filter out Enterprise apps from the menu"""
        apps = super().get_apps_menu()
        # Filter out apps that require Enterprise (to_buy = True)
        filtered_apps = []
        for app in apps:
            if not app.get('to_buy', False):
                filtered_apps.append(app)
        return filtered_apps


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def get_frontend_session_info(self):
        """Override session info to modify apps list"""
        session_info = super().get_frontend_session_info()
        
        # Filter apps in session info
        if 'apps' in session_info:
            filtered_apps = []
            for app in session_info['apps']:
                # Skip Enterprise apps
                if not app.get('to_buy', False):
                    filtered_apps.append(app)
            session_info['apps'] = filtered_apps
            
        return session_info


class MenuService(models.AbstractModel):
    _inherit = 'ir.ui.menu'

    @api.model
    def load_menus(self, debug=False):
        """Override to filter Enterprise apps from menu loading"""
        result = super().load_menus(debug)
        
        # Filter out Enterprise apps from apps list
        if 'apps' in result:
            filtered_apps = []
            for app in result['apps']:
                # Check if this is an Enterprise app
                module = self.env['ir.module.module'].search([
                    ('name', '=', app.get('appID', ''))
                ], limit=1)
                
                if not module.to_buy:
                    filtered_apps.append(app)
                    
            result['apps'] = filtered_apps
            
        return result

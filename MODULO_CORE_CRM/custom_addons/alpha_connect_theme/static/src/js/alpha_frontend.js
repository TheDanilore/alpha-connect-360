/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";

/**
 * Alpha Connect Frontend JS
 * 
 * Este script personaliza el frontend de Odoo para Alpha Connect:
 * - Reemplaza referencias a Odoo en el título
 * - Cambia el favicon
 * - Reemplaza textos en la interfaz
 */
const { Component, onMounted, onWillStart } = owl;

export class AlphaConnectFrontend extends Component {
    setup() {
        onWillStart(() => this._setupCustomizations());
        onMounted(() => this._applyCustomizations());
    }

    /**
     * Configuraciones iniciales
     */
    _setupCustomizations() {
        // Cambiar favicon
        this._setFavicon('/alpha_connect_theme/static/src/img/favicon.ico');
        
        // Cambiar título de la página
        document.title = document.title.replace(/Odoo/g, 'Alpha Connect');
    }

    /**
     * Aplicar personalizaciones cuando el DOM esté listo
     */
    _applyCustomizations() {
        // Reemplazar menciones a Odoo
        this._replaceOdooMentions();
        
        // Limpiar URLs
        this._cleanupURLs();
        
        // Ocultar copyright
        this._hideOdooCopyright();
    }

    /**
     * Cambiar el favicon del sitio
     */
    _setFavicon(iconPath) {
        let favicon = document.querySelector('link[rel="shortcut icon"]');
        if (!favicon) {
            favicon = document.createElement('link');
            favicon.rel = 'shortcut icon';
            document.head.appendChild(favicon);
        }
        favicon.href = iconPath;
    }

    /**
     * Reemplazar menciones a Odoo en textos
     */
    _replaceOdooMentions() {
        const walker = document.createTreeWalker(
            document.body, 
            NodeFilter.SHOW_TEXT, 
            null, 
            false
        );
        
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue.includes('Odoo') || node.nodeValue.includes('odoo')) {
                node.nodeValue = node.nodeValue
                    .replace(/Odoo/g, 'Alpha Connect')
                    .replace(/odoo/g, 'alpha connect');
            }
        }
    }

    /**
     * Limpiar URLs que contengan "odoo"
     */
    _cleanupURLs() {
        // Redireccionar URLs con /odoo/ a rutas limpias
        const currentPath = window.location.pathname;
        if (currentPath.includes('/odoo/')) {
            const newPath = currentPath.replace('/odoo/', '/');
            window.history.replaceState({}, document.title, newPath);
        }
        
        // Desactivar links a odoo.com
        document.querySelectorAll('a[href*="odoo.com"]').forEach(link => {
            link.href = '#';
            link.target = '';
            link.style.pointerEvents = 'none';
        });
    }

    /**
     * Ocultar copyright de Odoo
     */
    _hideOdooCopyright() {
        document.querySelectorAll('.o_footer_copyright_name').forEach(el => {
            if (el.textContent.includes('Odoo')) {
                el.textContent = '© ' + new Date().getFullYear() + ' Alpha Connect';
            }
        });
    }
}

// Registrar componente con Owl
AlphaConnectFrontend.template = 'alpha_connect_theme.AlphaConnectFrontend';

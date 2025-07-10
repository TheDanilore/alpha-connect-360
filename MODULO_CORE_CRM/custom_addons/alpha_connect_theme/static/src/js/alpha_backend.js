/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";

/**
 * Alpha Connect Backend JS
 * 
 * Este script personaliza el backend de Odoo para Alpha Connect:
 * - Reemplaza referencias a Odoo en el título
 * - Cambia el favicon
 * - Reemplaza textos en la interfaz
 * - Elimina URLs con "odoo"
 */
const { Component, onMounted, onWillStart } = owl;

export class AlphaConnectCustomizations extends Component {
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
        // Ejecutar cada segundo para asegurar que se apliquen en carga dinámica
        this._customizationInterval = browser.setInterval(() => {
            this._replaceBranding();
            this._cleanupURLs();
        }, 1000);
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
     * Reemplazar menciones a Odoo en la interfaz
     */
    _replaceBranding() {
        // Reemplazar textos
        this._replaceTextInElements('Odoo', 'Alpha Connect');
        
        // Ocultar elementos con copyright
        document.querySelectorAll('.o_footer_copyright, .o_brand_promotion').forEach(
            el => el.style.display = 'none'
        );
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
     * Reemplazar texto en todos los nodos
     */
    _replaceTextInElements(search, replace) {
        const walker = document.createTreeWalker(
            document.body, 
            NodeFilter.SHOW_TEXT, 
            null, 
            false
        );
        
        let node;
        const nodesToModify = [];
        
        // Recopilar nodos para evitar modificar durante el recorrido
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.includes(search)) {
                nodesToModify.push(node);
            }
        }
        
        // Modificar nodos
        nodesToModify.forEach(node => {
            node.nodeValue = node.nodeValue.replace(new RegExp(search, 'g'), replace);
        });
    }

    /**
     * Limpiar al desmontar el componente
     */
    willUnmount() {
        if (this._customizationInterval) {
            browser.clearInterval(this._customizationInterval);
        }
    }
}

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new AlphaConnectCustomizations();
});

// Alpha Connect 360 - Hide Enterprise Apps
// ========================================

(function() {
    'use strict';
    
    // Función para ocultar aplicaciones Enterprise
    function hideEnterpriseApps() {
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', hideEnterpriseApps);
            return;
        }
        
        // Función principal para ocultar elementos
        function processElements() {
            // 1. Ocultar botones de "Actualizar" y "Upgrade"
            const upgradeButtons = document.querySelectorAll('button, a, .btn');
            upgradeButtons.forEach(function(button) {
                const text = (button.textContent || button.innerText || '').toLowerCase();
                const href = button.getAttribute('href') || '';
                
                if (text.includes('upgrade') || 
                    text.includes('actualizar') ||
                    text.includes('buy now') ||
                    text.includes('comprar') ||
                    href.includes('upgrade') ||
                    href.includes('buy')) {
                    
                    button.style.display = 'none';
                    
                    // También ocultar el contenedor padre si es necesario
                    const parent = button.closest('.oe_button_box, .o_kanban_button_new');
                    if (parent) {
                        parent.style.display = 'none';
                    }
                }
            });
            
            // 2. Ocultar aplicaciones con botones de upgrade
            const appCards = document.querySelectorAll('.o_app, .oe_module_vignette');
            appCards.forEach(function(card) {
                // Buscar botones de upgrade dentro de la card
                const upgradeBtn = card.querySelector('button[data-original-title*="upgrade"], button[title*="upgrade"], .btn:contains("Upgrade"), .btn:contains("Actualizar")');
                const upgradeText = card.querySelector('*[class*="upgrade"], *[class*="enterprise"]');
                
                if (upgradeBtn || upgradeText) {
                    card.style.display = 'none';
                }
                
                // También verificar por texto en la descripción
                const description = card.querySelector('.o_app_summary, .oe_module_desc');
                if (description) {
                    const descText = description.textContent.toLowerCase();
                    if (descText.includes('enterprise') || descText.includes('upgrade required')) {
                        card.style.display = 'none';
                    }
                }
            });
            
            // 3. Ocultar paneles específicos de Enterprise
            const enterprisePanels = document.querySelectorAll([
                '.o_enterprise_app_panel',
                '.o_enterprise_upsell',
                '.o_upgrade_banner',
                '.o_enterprise_promotion',
                '*[data-enterprise="true"]',
                '*[class*="enterprise"]'
            ].join(', '));
            
            enterprisePanels.forEach(function(panel) {
                panel.style.display = 'none';
            });
            
            // 4. Filtrar dropdown de aplicaciones en el navbar
            const appDropdownItems = document.querySelectorAll('.o_app, .dropdown-item[data-menu-xmlid]');
            appDropdownItems.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes('upgrade') || text.includes('enterprise')) {
                    item.style.display = 'none';
                }
            });
        }
        
        // Ejecutar inmediatamente
        processElements();
        
        // Observar cambios en el DOM para aplicaciones SPA
        const observer = new MutationObserver(function(mutations) {
            let shouldProcess = false;
            
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Verificar si se agregaron elementos relevantes
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            const hasRelevantClass = node.classList && (
                                node.classList.contains('o_app') ||
                                node.classList.contains('o_kanban_view') ||
                                node.classList.contains('o_apps') ||
                                node.querySelector && node.querySelector('.o_app, .btn, button')
                            );
                            
                            if (hasRelevantClass) {
                                shouldProcess = true;
                            }
                        }
                    });
                }
            });
            
            if (shouldProcess) {
                setTimeout(processElements, 100);
            }
        });
        
        // Observar cambios en el body
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Ejecutar en cambios de ruta para SPA
        let lastUrl = location.href;
        new MutationObserver(function() {
            const url = location.href;
            if (url !== lastUrl) {
                lastUrl = url;
                setTimeout(processElements, 500);
            }
        }).observe(document, {subtree: true, childList: true});
        
        // También ejecutar en eventos de navegación
        window.addEventListener('hashchange', function() {
            setTimeout(processElements, 500);
        });
        
        window.addEventListener('popstate', function() {
            setTimeout(processElements, 500);
        });
        
        // Ejecutar periódicamente como respaldo
        setInterval(processElements, 3000);
    }
    
    // Inicializar cuando esté listo
    hideEnterpriseApps();
    
})();

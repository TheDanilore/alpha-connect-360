/**
 * Enhanced URL Fixer script for database manager
 * This script is injected directly into the database manager page
 * to fix any /odoo redirects
 */
document.addEventListener("DOMContentLoaded", function () {
    console.log('Database Manager URL Fixer loaded');
    
    // Fix links to databases - more aggressive selection
    function fixAllLinks() {
        // Fix direct links to /odoo
        const dbLinks = document.querySelectorAll('a[href^="/odoo"]');
        for (const link of dbLinks) {
            console.log('Found database link:', link.href);
            link.href = link.href.replace('/odoo', '/web/login');
            console.log('Fixed to:', link.href);
        }
        
        // Fix links with db parameter
        const dbParamLinks = document.querySelectorAll('a[href*="db="]');
        for (const link of dbParamLinks) {
            if (link.href.includes('/odoo?db=')) {
                console.log('Found database param link:', link.href);
                link.href = link.href.replace('/odoo?db=', '/web/login?db=');
                console.log('Fixed to:', link.href);
            }
        }
        
        // Fix other potential links
        const allLinks = document.querySelectorAll('a');
        for (const link of allLinks) {
            if (link.getAttribute('data-db')) {
                link.addEventListener('click', function(e) {
                    console.log('Intercepting data-db link click');
                    const db = this.getAttribute('data-db');
                    if (db) {
                        e.preventDefault();
                        window.location.href = '/web/login?db=' + db;
                    }
                });
            }
        }
    }
    
    // Run immediately and also after a short delay (for dynamic content)
    fixAllLinks();
    setTimeout(fixAllLinks, 500);
    
    // Override window.location functions
    const originalAssign = window.location.assign;
    const originalReplace = window.location.replace;
    const originalHref = Object.getOwnPropertyDescriptor(window.location, 'href');
    
    window.location.assign = function(url) {
        console.log('Intercepting location.assign:', url);
        if (url && typeof url === 'string') {
            if (url.includes('/odoo?db=')) {
                url = url.replace('/odoo?db=', '/web/login?db=');
            } else if (url.includes('/odoo')) {
                url = url.replace('/odoo', '/web');
            }
            console.log('Fixed URL to:', url);
        }
        return originalAssign.call(window.location, url);
    };
    
    window.location.replace = function(url) {
        console.log('Intercepting location.replace:', url);
        if (url && typeof url === 'string') {
            if (url.includes('/odoo?db=')) {
                url = url.replace('/odoo?db=', '/web/login?db=');
            } else if (url.includes('/odoo')) {
                url = url.replace('/odoo', '/web');
            }
            console.log('Fixed URL to:', url);
        }
        return originalReplace.call(window.location, url);
    };
    
    // Monitor all link clicks
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.href) {
            if (link.href.includes('/odoo?db=')) {
                console.log('Intercepting link click with DB:', link.href);
                e.preventDefault();
                let newUrl = link.href.replace('/odoo?db=', '/web/login?db=');
                console.log('Redirecting to:', newUrl);
                window.location.href = newUrl;
            } else if (link.href.includes('/odoo')) {
                console.log('Intercepting link click:', link.href);
                e.preventDefault();
                let newUrl = link.href.replace('/odoo', '/web');
                console.log('Redirecting to:', newUrl);
                window.location.href = newUrl;
            }
        }
    }, true);
    
    // Monitor form submissions
    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (form && form.action) {
            if (form.action.includes('/odoo')) {
                console.log('Intercepting form submit:', form.action);
                e.preventDefault();
                let newAction = form.action.replace('/odoo', '/web');
                console.log('Changing form action to:', newAction);
                form.action = newAction;
                form.submit();
            }
        }
    }, true);
    
    console.log('Enhanced Database Manager URL Fixer initialization complete');
});

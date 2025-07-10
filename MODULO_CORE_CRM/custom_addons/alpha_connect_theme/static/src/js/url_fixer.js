/**
 * Enhanced URL Fixer for Alpha Connect 360
 * 
 * This script intercepts and fixes any URLs that contain /odoo to use /web instead.
 * Enhanced version to handle more edge cases and be more aggressive in URL fixing.
 */
odoo.define('alpha_connect_theme.url_fixer', function (require) {
    "use strict";

    console.log('Enhanced URL Fixer loaded');
    
    // Fix all links in the document
    function fixAllLinks() {
        const links = document.querySelectorAll('a[href*="/odoo"]');
        for (const link of links) {
            console.log('Found /odoo link:', link.href);
            if (link.href.includes('/odoo?db=')) {
                link.href = link.href.replace('/odoo?db=', '/web/login?db=');
            } else if (link.href.includes('/odoo/apps')) {
                link.href = link.href.replace('/odoo/apps', '/web/apps');
            } else {
                link.href = link.href.replace('/odoo', '/web');
            }
            console.log('Fixed to:', link.href);
        }
    }
    
    // Run immediately and also periodically
    fixAllLinks();
    setInterval(fixAllLinks, 2000); // Check every 2 seconds
    
    // Override window.location functions
    const originalAssign = window.location.assign;
    const originalReplace = window.location.replace;
    
    window.location.assign = function(url) {
        console.log('Intercepting location.assign:', url);
        if (url && typeof url === 'string') {
            if (url.includes('/odoo?db=')) {
                url = url.replace('/odoo?db=', '/web/login?db=');
            } else if (url.includes('/odoo/apps')) {
                url = url.replace('/odoo/apps', '/web/apps');
            } else if (url.includes('/odoo')) {
                url = url.replace('/odoo', '/web');
            }
            console.log('Fixed URL:', url);
        }
        return originalAssign.call(window.location, url);
    };
    
    window.location.replace = function(url) {
        console.log('Intercepting location.replace:', url);
        if (url && typeof url === 'string') {
            if (url.includes('/odoo?db=')) {
                url = url.replace('/odoo?db=', '/web/login?db=');
            } else if (url.includes('/odoo/apps')) {
                url = url.replace('/odoo/apps', '/web/apps');
            } else if (url.includes('/odoo')) {
                url = url.replace('/odoo', '/web');
            }
            console.log('Fixed URL:', url);
        }
        return originalReplace.call(window.location, url);
    };
    
    // Override Object.defineProperty for window.location.href
    try {
        const originalHrefDescriptor = Object.getOwnPropertyDescriptor(window.location, 'href');
        
        if (originalHrefDescriptor && originalHrefDescriptor.set) {
            Object.defineProperty(window.location, 'href', {
                set: function(url) {
                    console.log('Intercepting location.href set:', url);
                    if (url && typeof url === 'string') {
                        if (url.includes('/odoo?db=')) {
                            url = url.replace('/odoo?db=', '/web/login?db=');
                        } else if (url.includes('/odoo/apps')) {
                            url = url.replace('/odoo/apps', '/web/apps');
                        } else if (url.includes('/odoo')) {
                            url = url.replace('/odoo', '/web');
                        }
                        console.log('Fixed URL:', url);
                    }
                    return originalHrefDescriptor.set.call(window.location, url);
                },
                get: originalHrefDescriptor.get,
                configurable: true
            });
        }
    } catch (e) {
        console.error('Failed to override window.location.href:', e);
    }
    
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
            } else if (link.href.includes('/odoo/apps')) {
                console.log('Intercepting link click to apps:', link.href);
                e.preventDefault();
                let newUrl = link.href.replace('/odoo/apps', '/web/apps');
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
    
    // Override history.pushState and history.replaceState
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;
    
    history.pushState = function(state, title, url) {
        console.log('Intercepting history.pushState:', url);
        if (url && typeof url === 'string') {
            if (url.includes('/odoo?db=')) {
                url = url.replace('/odoo?db=', '/web/login?db=');
            } else if (url.includes('/odoo/apps')) {
                url = url.replace('/odoo/apps', '/web/apps');
            } else if (url.includes('/odoo')) {
                url = url.replace('/odoo', '/web');
            }
            console.log('Fixed URL:', url);
        }
        return originalPushState.call(history, state, title, url);
    };
    
    history.replaceState = function(state, title, url) {
        console.log('Intercepting history.replaceState:', url);
        if (url && typeof url === 'string') {
            if (url.includes('/odoo?db=')) {
                url = url.replace('/odoo?db=', '/web/login?db=');
            } else if (url.includes('/odoo/apps')) {
                url = url.replace('/odoo/apps', '/web/apps');
            } else if (url.includes('/odoo')) {
                url = url.replace('/odoo', '/web');
            }
            console.log('Fixed URL:', url);
        }
        return originalReplaceState.call(history, state, title, url);
    };
    
    // Monitor form submissions
    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (form && form.action) {
            if (form.action.includes('/odoo?db=')) {
                console.log('Intercepting form submit with DB:', form.action);
                e.preventDefault();
                let newAction = form.action.replace('/odoo?db=', '/web/login?db=');
                console.log('Changing form action to:', newAction);
                form.action = newAction;
                form.submit();
            } else if (form.action.includes('/odoo/apps')) {
                console.log('Intercepting form submit to apps:', form.action);
                e.preventDefault();
                let newAction = form.action.replace('/odoo/apps', '/web/apps');
                console.log('Changing form action to:', newAction);
                form.action = newAction;
                form.submit();
            } else if (form.action.includes('/odoo')) {
                console.log('Intercepting form submit:', form.action);
                e.preventDefault();
                let newAction = form.action.replace('/odoo', '/web');
                console.log('Changing form action to:', newAction);
                form.action = newAction;
                form.submit();
            }
        }
    }, true);
    
    // Override AJAX requests
    if (window.XMLHttpRequest) {
        const originalOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
            if (url && typeof url === 'string') {
                if (url.includes('/odoo?db=')) {
                    url = url.replace('/odoo?db=', '/web/login?db=');
                } else if (url.includes('/odoo/apps')) {
                    url = url.replace('/odoo/apps', '/web/apps');
                } else if (url.includes('/odoo')) {
                    url = url.replace('/odoo', '/web');
                }
            }
            return originalOpen.call(this, method, url, async, user, password);
        };
    }
    
    // Override fetch API
    if (window.fetch) {
        const originalFetch = window.fetch;
        window.fetch = function(resource, init) {
            if (resource && typeof resource === 'string') {
                if (resource.includes('/odoo?db=')) {
                    resource = resource.replace('/odoo?db=', '/web/login?db=');
                } else if (resource.includes('/odoo/apps')) {
                    resource = resource.replace('/odoo/apps', '/web/apps');
                } else if (resource.includes('/odoo')) {
                    resource = resource.replace('/odoo', '/web');
                }
            }
            return originalFetch.call(this, resource, init);
        };
    }
    
    console.log('Enhanced URL Fixer initialization complete');
});

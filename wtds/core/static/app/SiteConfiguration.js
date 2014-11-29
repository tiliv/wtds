angular.module('wtds.services.SiteConfiguration', [])

.factory('SiteConfiguration', function(){
    return {
        STATIC_URL: window._STATIC_URL,
        TEMPLATE_URL: window._STATIC_URL + 'templates/'
    }
})

angular.module('wtds.api', ['restangular'])

.config(function(RestangularProvider){
    RestangularProvider.setBaseUrl('/api');
    RestangularProvider.setRequestSuffix('/');
})

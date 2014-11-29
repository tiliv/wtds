var wallpapers = angular.module('wtds.wallpapers', [
    'wtds.api',
    'wtds.services.SiteConfiguration'
])

.controller('WallpaperList', function($scope, Restangular){
    this.apiSource = Restangular.all('wallpapers').getList();
    $scope.objects = this.apiSource.$object;  // to be filled when api call finishes
})

.directive('wallpaperList', function(SiteConfiguration){
    return {
        restrict: 'E',
        templateUrl: SiteConfiguration.TEMPLATE_URL + 'wallpapers/wallpaper_list.html'
    }
})
.directive('wallpaperTile', function(SiteConfiguration){
    return {
        restrict: 'E',
        // require: '^WallpaperList',
        templateUrl: SiteConfiguration.TEMPLATE_URL + 'wallpapers/wallpaper_tile.html',
        scope: {
            "wallpaper": '='
        }
    }
})
.directive('tagList', function(SiteConfiguration){
    return {
        restrict: 'E',
        templateUrl: SiteConfiguration.TEMPLATE_URL + 'wallpapers/tag_list.html',
        scope: {
            "objects": '='
        }
    }
})
.directive('tag', function(SiteConfiguration){
    return {
        restrict: 'E',
        // require: '^TagList',
        templateUrl: SiteConfiguration.TEMPLATE_URL + 'wallpapers/tag.html',
        scope: {
            "tag": '='
        }
    }
})

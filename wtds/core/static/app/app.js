var app = angular.module('wtds', ['wtds.services.HttpQueue'])

// .controller('', function(){
// })

.run(function(HttpQueue){
    function init(){
        HttpQueue.getAll([
            // 'landing.html'
        ]);
    }

    init();
});

angular.module('wtds.services.HttpQueue', [])

.factory('HttpQueue', function($q, $http){
    var queue = [];

    var utils = {
        "setupRequest": function(uri, config){
            // Assign the request a promise

            console.debug("Building formal request object for", uri);
            uri = utils.formatUri(uri);
            return {
                // 'request' object is sent straight into $http getter
                "request": {
                    "url": uri,
                    "config": config
                },
                "deferred": $q.defer()
            }
        },
        "formatUri": function(uri){
            // Ensure the uri string is a fully qualified url
            var originalUri = uri;
            if (!/^(https?:)\/\//.test(uri)) {
                if (!/^\//.test(uri)) {
                    console.debug("Prepending", window.location.pathname, "to", originalUri);
                    uri = window.location.pathname + uri;
                }
                if (!(new RegExp(window.location.host).test(uri))) {
                    uri = window.location.host + uri;
                }
                uri = window.location.protocol + "//" + uri;
                console.debug("Formatted", originalUri, "to", uri);
            }
            return uri;
        }
    }

    function fetch(){
        // Starts a request loop until the queue is empty
        console.debug("Items in request queue:", queue.length);

        var item = queue.shift();
        console.debug("Fetching", item);

        $http(item.request).then(function(data){
            item.deferred.resolve(data);
        }, function(data){
            console.error(data);
            item.deferred.reject(data);
        }).finally(function(){
            if (queue.length > 0) {
                fetch();
            }
        });
    }
    function addRequest(uri, config){
        return addRequests([uri], config);
    }
    function addRequests(uriList, config){
        // Adds all ``uriList`` to end of queue
        // Returns a promise that completes when all configs are finished.
        console.debug("Adding", uriList.length, uriList);

        function _setupRequest(uri){
            return utils.setupRequest(uri, config);
        }

        var requests = $.map(uriList, _setupRequest);
        queue.push.apply(queue, requests);

        if (queue.length > 0) {
            fetch();
        }

        return $q.all($.map(requests, function(request){
            return request.deferred;
        }));
    }

    return {
        "get": addRequest,
        "getAll": addRequests,
        "isProcessing": function(){return queue.length > 0}
    };
});

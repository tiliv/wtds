// Helpers for other script files
var _resize_callback = null;
function set_resize_callback(callback) {
    _resize_callback = callback;
}
var ASPECT_RATIO_SPECIAL_CASES = {
    '8:5': '16:10'
}

// Bind a throttled window resize event that calls the callback set by the utility above.
$(function(){
    var resize_throttle_id = null;
    $(window).on('resize', function(){
        if (resize_throttle_id === null) {
            resize_throttle_id = setTimeout(function(){
                resize_throttle_id = null;
                if (pending_event) {
                    $(window).resize(); // Let a pending event through
                }
            }, 100);

            (_resize_callback || function(){})();
            pending_event = false;
        } else {
            // Rate-limited; do nothing
            pending_event = true;
        }
    });
});

// Depends on: (* represents project resource)
// jQuery
// calculate-gcd-javascript.js (gcd function)
// *resize.js

$(function(){
    var image_tag = $('#stage img')[0];
    var SHOWING_SIZE_READOUT = $('#details .size .showing');

    setTimeout(function(){display_size_scale()}, 100);
    function display_size_scale() {
        var percentage = 100 * image_tag.width / image_tag.naturalWidth;
        SHOWING_SIZE_READOUT.text(Math.round(percentage));
    }
    set_resize_callback(display_size_scale);
});

// Depends on:
// jQuery
// calculate-gcd-javascript.js (gcd function)

$(document).ready(function(){
    var dndSupported = function () {
      var div = document.createElement('div');
      return ('draggable' in div) || ('ondragstart' in div && 'ondrop' in div);
    };

    var acceptedTypes = {
        'image/png': true,
        'image/jpeg': true,
        'image/gif': true
    };

    var aspect_ratio_special_cases = {
        '8:5': '16:10'
    }

    var HOVER_CLASS = 'hover';
    var FORM = $('form');
    var HOVER_INDICATOR = $('#hover-indicator');
    var PREVIEW_STAGE = $('#preview-stage');
    var RESIZE_READOUT = $('#size-readout');

    var image_tag = null;
    var image_data = null;

    function enableDragEvents() {
        HOVER_INDICATOR.text("Drop image file anywhere on the page");
        var droptarget = HOVER_INDICATOR;
        $('body')[0].ondragover = function(){
            droptarget.addClass(HOVER_CLASS);
            return false;
        }
        droptarget[0].ondragend = droptarget[0].ondragleave = function(){
            droptarget.removeClass(HOVER_CLASS);
            return false;
        }
        droptarget[0].ondrop = function(event){
            // Stop the browser from responding (navigating) to the dropped file
            event.preventDefault && event.preventDefault();

            droptarget.removeClass(HOVER_CLASS);
            handleImage(event.dataTransfer.files[0]);

            return false;
        }
    }
    function disableDragEvents() {
        $('body')[0].ondragover = null;
        HOVER_INDICATOR.ondragend = null;
        HOVER_INDICATOR.ondragleave = null;
        HOVER_INDICATOR.ondrop = null;
    }
    function handleImage(file) {
        image_data = file;
        if (acceptedTypes[file.type] === true) {
            var reader = new FileReader();
            reader.onload = function (event) {
                image_tag = new Image();
                image_tag.src = event.target.result;
                PREVIEW_STAGE.append(image_tag);

                // Give the DOM a brief delay to respond to automatic CSS width sizing
                setTimeout(function(){
                    activateHelpers();
                    replaceTraditionalImageInputField();
                    disableDragEvents();
                    bindFormSubmissionListener();
                }, 100);
            };
            reader.readAsDataURL(image_data);
        }
    }
    function activateHelpers() {
        updateInfoLabel();
        var resize_throttle_id = null;
        var pending_event = false;
        $(window).resize(function(){
            if (resize_throttle_id === null) {
                resize_throttle_id = setTimeout(function(){
                    resize_throttle_id = null;
                    if (pending_event) {
                        $(window).resize(); // Let a pending event through
                    }
                }, 100);

                // Update the label
                updateInfoLabel();
                pending_event = false;
            } else {
                // Rate-limited; do nothing
                pending_event = true;
            }
        });
    }
    function updateInfoLabel() {
        var percentage = 100 * image_tag.width / image_tag.naturalWidth;
        var divisor = gcd(image_tag.naturalWidth, image_tag.naturalHeight);
        var ratio_width = image_tag.naturalWidth / divisor;
        var ratio_height = image_tag.naturalHeight / divisor;
        var ratio = '' + ratio_width + ':' + ratio_height;
        if (aspect_ratio_special_cases[ratio]) {
            ratio = aspect_ratio_special_cases[ratio];
        }

        var s = '' + Math.round(percentage) + '% actual size';
        s += ' ('+image_tag.naturalWidth+'&times;'+image_tag.naturalHeight+')';
        s += '; <strong>Aspect ratio</strong>: ' + ratio;
        RESIZE_READOUT.html(s);
    }
    function replaceTraditionalImageInputField() {
        // Destroys the normal file picker and sets up the #preview-stage to stand in its place.
        var input = $('#id_image');
        PREVIEW_STAGE.attr('data-name', input.attr('name'));
        input.closest('p').slideUp(function(){ $(this).remove(); });
    }
    function bindFormSubmissionListener() {
        // Attach submission event for slipping the stage's image data into a hidden field.
        FORM.on('submit', function(){
            var field_name = PREVIEW_STAGE.attr('data-name') + '_raw';
            var image_data = PREVIEW_STAGE.find('img').attr('src')
            var image_raw = $('<input type="hidden" />').attr('name', field_name).val(image_data);
            FORM.append(image_raw);
            return true;
        });
    }

    // Bind drag events
    if (!dndSupported()) {
        $('#id_image').show().change(function(){
            handleImage(this.files[0]);
        });
    } else {
        enableDragEvents();
    }
});

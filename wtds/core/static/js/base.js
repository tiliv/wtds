$(function(){
    var _actives = null;
    $('.show-tags-button').on('click', function(){
        var button = $(this);
        var toggle_off = button.hasClass("showing");
        if (_actives) {
            _actives.removeClass("showing"); // css transition begins
            if (!toggle_off) {
                // As long as the clicked element isn't just being deactivated, set up a callback that sets the 'display: none' property on the tags popup.  If done in CSS, the opactiy transition effect is completely subverted.
                // This is an inline function call to create a closure holding the deactivated .tags element, in case the user is click-spamming and _actives changes before the timeout callback can run.
                setTimeout((
                    function(tags){
                        // The real setTimeout callback:
                        return function(){ tags.css('display', 'none'); };
                    })(_actives.filter('.tags')), 200);
            }
        }
        if (toggle_off) {
            _actives = null;
        } else {
            _actives = button.add(button.siblings('.tags').css('display', 'block')).toggleClass("showing");
        }
    });

    // pjax handlers
    var content = $('#pjax-wrapper');
    $(document).pjax('#lineup .wallpaper.tile', '#pjax-wrapper');
    $(document).on('pjax:start', function(event, xhr, options) {
        var image = $(options.target).find('img');
        // Fade away other images
        image.closest('.tile-wrapper').siblings('.tile-wrapper').addClass('blur');

        // Zoom selected image
        image[0].src = image.attr('data-raw-url');
        var original_width = image.attr('data-real-width');
        render_width = .65 * content.width();
        image.css({
            'width': render_width,
            'height': image.attr('data-real-height') / (original_width / render_width)
        });
        image.offset({'top': 169, 'left': 32});
    })
    $(document).on('pjax:send', function() {
        console.log("send");
    })
    $(document).on('pjax:complete', function() {
        console.log("complete");
    })
    $(document).on('pjax:end', function() {
        console.log("end");
    })
    $(document).on('pjax:timeout', function(event) {
      // Prevent default timeout redirection behavior
      event.preventDefault()
    })
});

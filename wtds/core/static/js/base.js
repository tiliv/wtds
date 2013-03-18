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

    var wrapper_id = '#wrapped-content';
    var content = $(wrapper_id);
    var stage = $('#stage');
    var TRANSITION_TIME = 500 // ms

    // Bad, bad magic numbers
    var DETAIL_TOP = 211;
    var DETAIL_LEFT = 32;
    var TILE_WIDTH = 140;
    var TILE_HEIGHT = 94;

    // jQuery events won't forward properties they don't know about, I guess (?)
    // Add the state property to jQuery's event object so we can use it in
    // $(window).bind('popstate')
    if ($.inArray('state', $.event.props) == -1) {
        $.event.props.push('state')
    }

    // push/pop handlers
    content.on('click', '#lineup .wallpaper.tile', function(){
        var link = $(this);

        // Set the current state before we go pushing a new one
        history.replaceState({
            'view': 'list',
            'content': content.html(),
            'data-id': link.attr('data-id')
        });
        
        // Push the new page state (blank--will be popped away when the user pressed Back).
        history.pushState({
            'view': 'detail',
            'content': null, // replaced when the ajax completes
            'data-id': link.attr('data-id')
        }, '', this.pathname);

        // Animate
        zoomTo(history.state);

        return false;
    });
    $(window).on('popstate', function(event){
        if (event.state) {
            if (event.state.view == "list") {
                zoomBack(event.state);
            } else if (event.state.view == "detail") {
                zoomTo(event.state);
            }
        }
    });

    // push/pop animators
    function zoomTo(state) {
        // Fade away other images and zoom the clicked tile to its "detail" size.
        content.addClass('blur');

        var tile = content.find('[data-id='+state['data-id']+']');

        var new_image = new Image();
        var image = null;
        image = $(tile).find('img');
        
        var offset = image.offset();
        new_image.src = image[0].src;
        transitioning_image = $(new_image).attr('id', 'transitioning').insertAfter(content);
        transitioning_image.offset(offset).data({
            'thumbnail_id': image.attr('id')
        }).css({
            'width': image.width(),
            'height': image.height()
        }).attr({
            'data-thumbnail-url': image[0].src,
        });
        
        // Zoom selected image
        // This is slightly more complex than just scaling up the thumbnail's dimensions, because we normalize all thumbnail tiles to a 16:10 aspect ratio, while the raw image isn't guaranteed to even be in a landscape orientation.
        new_image.src = image.attr('data-raw-url');
        var original_width = image.attr('data-real-width');
        render_width = .65 * content.width();
        $(new_image).attr('id', 'transitioning').css({
            'transition': TRANSITION_TIME + 'ms ease',
            'width': render_width,
            'height': image.attr('data-real-height') / (original_width / render_width),
            'top': DETAIL_TOP,
            'left': DETAIL_LEFT
        });

        // Do the work
        function complete(data) {
            content.html(data);
            content.removeClass('blur');
            history.replaceState({
                'view': 'detail',
                'content': data,
                'data-id': state['data-id']
            }, '', tile[0].pathname);
        }
        if (!event.content) {
            $.get(tile[0].pathname, complete);
        } else {
            // console.log('nolookup')
            complete(event.content);
        }

        // This is currently on a slght delay because too much happens too quickly, and performance goes down the crapper instead of seeing a nice transition.  This allows for the ajax load to take at least as long as the transition time (200ms).  The delay is harmless if the ajax takes longer than that.
        setTimeout(function(){
            stage.append(transitioning_image);
            
            // Remove transient css data so that we're left with a clean dom element
            transitioning_image.removeAttr('id').css({
                'transition': '',
                'width': '',
                'height': '',
                'top': '',
                'left': ''
            });
        }, TRANSITION_TIME);
    }
    function zoomBack(state) {
        // Uses the history stack to zoom back to the targetted image in a #lineup

        // Find and move the image out of the stage
        var transitioning_image = $('#stage img');
        var width = transitioning_image.width();
        var height = transitioning_image.height();
        // Bake current position into css so that nothing jumps around during css transitions
        transitioning_image.attr('id', 'transitioning').offset(transitioning_image.offset());
        transitioning_image.css({
            'width': width,
            'height': height
        })[0].src = transitioning_image.attr('data-thumbnail-url');
        transitioning_image.insertAfter(content);

        // Instantly dump the details page content and unblur the list view
        content.empty().css('transition', 'none');
        content.addClass('blur');
        content.html(state.content);
        setTimeout(function(){
            content.css('transition', '').removeClass('blur');
        }, TRANSITION_TIME);
        
        // Locate the tile's target position
        // This is rediscovered at runtime in case the user has resized their window since clicking on the tile to navigate to the details view.
        var target_tile = content.find('.tile[data-id='+state['data-id']+']');

        // Animate to old tile position and revert to thumbnail image instead of full-res image
        transitioning_image.offset(target_tile.offset()).css({
            'transition': TRANSITION_TIME + 'ms ease',
            'width': TILE_WIDTH,
            'height': TILE_HEIGHT
        });
        

        setTimeout(function(){
            transitioning_image.remove();
            transitioning_image = null;
        }, TRANSITION_TIME);
    }
});

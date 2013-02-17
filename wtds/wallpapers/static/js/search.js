var search_input;

function trigger_filter() {
    if (search_input) { // ignore the initial tagsinput construction
        search_input.trigger('search.wtds');
    }
}

$(function(){
    var search_bar = $('#search-bar');
    var search_url = search_bar.attr('action');
    search_input = search_bar.find('input[name=terms]');
    search_bar.find('button[rel=clear]').on('click', function(){
        search_input.importTags('');
    });
    // search_bar.find('button[rel=search]').on('click', function(){
    //     search_input.trigger('change');
    // });

    search_input.on('search.wtds', function(){
        var tags = search_input.val().split(',');
        var terms = [];
        for (var i in tags) {
            terms.push({'name': 'tag', 'value': tags[i]});
        }
        var url = search_url + '?' + $.param(terms);
        window.location = url;
    });
});

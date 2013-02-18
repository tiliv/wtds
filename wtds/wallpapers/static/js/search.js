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
        if (search_input.val() != '') {
            search_input.importTags('');
        }
        return false;
    });
    // search_bar.find('button[rel=search]').on('click', function(){
    //     search_input.trigger('change');
    // });

    search_input.on('search.wtds', function(){
        var terms = search_input.val().split(',');
        var tags = [];
        for (var i in terms) {
            tags.push({'name': 'tag', 'value': terms[i]});
        }
        var url = search_url + '?' + $.param(tags);
        window.location = url;
    });
});

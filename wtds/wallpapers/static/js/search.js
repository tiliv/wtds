var search_input;

function trigger_filter() {
    search_input.trigger('change')
}

$(function(){
    var search_bar = $('#search-bar');
    search_input = search_bar.find('input[name=terms]');
    search_bar.find('button[rel=clear]').on('click', function(){
        search_input.importTags('');
    });
    search_bar.find('button[rel=search]').on('click', function(){
        search_input.trigger('change');
    });

    search_input.on('change', function(){
        $(this).trigger('search.wtds');
    }).on('search.wtds', function(){
        console.log("values:", $(this).val());
    });
});

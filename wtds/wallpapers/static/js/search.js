$(function(){
    var search_bar = $('#search-bar');
    var search_input = search_bar.find('input[name=terms]');
    search_bar.find('button[rel=clear]').on('click', function(){
        search_input.importTags('');
    });
});

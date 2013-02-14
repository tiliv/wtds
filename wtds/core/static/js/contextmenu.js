/*
Handles context menu events.

Currently this only works in Firefox.  No other browsers have implemented it.

*/

var contextmenu = null;
var contextmenu_tags = null;
var _menuitem_tag_template = $('<menuitem label="" data-url=""></menuitem>');

$(function(){
    contextmenu = $('menu#tile-options');
    contextmenu_tags = $('menu#tile-options menu#contextmenu-tags');

    contextmenu.find('menuitem.download').on('click', function(){
        window.location = $(this).attr('data-url');
    });

    $('.wallpaper.tile').on('contextmenu', function(){
        var tile = $(this);
        var tags = [];
        tile.closest('.tile-wrapper').find('.tag').each(function(){
            var tag = $(this);
            var attrs = {'label': tag.attr('data-name'), 'data-url': tag.attr('href')};
            if (tag.hasClass('sketchy')) {
                attrs.icon = "/static/img/sketchy-warning.png";
            } else if (tag.hasClass('nsfw')) {
                attrs.icon = "/static/img/nsfw-warning.png"
            }
            tags.push(attrs);
        });
        tags.push('---');
        tags.push({'label': "Search on all tags", 'action': tile.attr('data-full-search-url')});
        
        set_wallpaper_contextmenu(tile.attr('data-download-url'), tags);
        return true;
    });
});

function set_wallpaper_contextmenu(download_url, tags) {
    contextmenu.attr('data-url', download_url);

    contextmenu_tags.empty();
    for (var i in tags) {
        var menuitem;
        if (tags[i] == "---") {
            menuitem = $("<hr />");
        } else {
            menuitem = _menuitem_tag_template.clone().attr(tags[i]);
            menuitem.on('click', function(){ window.location = $(this).attr('data-url'); });
        }
        contextmenu_tags.append(menuitem);
    }
}

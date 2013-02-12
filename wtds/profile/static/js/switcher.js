$(function(){
    var form = $('#profile-switch-form');
    form.find('select').change(function(){
        form.submit();
    })
});

$(function(){
    var form = $('form#account-control');
    form.find('select').change(function(){
        form.submit();
    })
});

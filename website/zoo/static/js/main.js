// main.js
function change_button(baseurl,original,endurl) {
    var fixed = original.replace(/ /g,'_');
    window.location.href = baseurl+fixed+endurl;
}

function show_overlay(obj) {
    id = "overlay-" + obj;
    document.getElementById(id).className = "overlay";
    id = obj + "-text";
    document.getElementById(id).style.maxHeight = (window.innerHeight - 250) + "px";
}

function hide_overlay(obj) {
    id = "overlay-" + obj;
    document.getElementById(id).className = "overlay hide";
}


$('input.limit-habitats').on('change', function(e) {
// limit to 10
    if($('.limit-habitats').filter(':checked').length >= 10) {
        $('.limit-habitats:not(:checked)').attr('disabled','disabled');
    } else {
        $('.limit-habitats').removeAttr("disabled");
    }
});

$('input.limit-regions').on('change', function(e) {
// limit to 10
    if ($('.limit-regions').filter(':checked').length >= 10) {
        $('.limit-regions:not(:checked)').attr('disabled','disabled');
    } else {
        $('.limit-regions').removeAttr("disabled");
    }
});

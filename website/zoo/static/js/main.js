$(document).ready(function() {
    $('#pagination').DataTable();
});

function change_link(obj,baseurl) {
    var original = obj.innerHTML; // without underscores
    var fixed = original.replace(/ /g,'_'); // with underscores
    window.location.href = baseurl+fixed+'/';
}

function change_button(baseurl,original,endurl) {
    var fixed = original.replace(/ /g,'_');
    window.location.href = baseurl+fixed+endurl;
}

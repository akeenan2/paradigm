$(document).ready(function() {
    $('#pagination').DataTable();
});

function change_link(obj,baseurl) {
    var original = obj.innerHTML; // without underscores
    var fixed = original.replace(/ /g,'_'); // with underscores
    obj.setAttribute('href',baseurl+fixed+'/');
}

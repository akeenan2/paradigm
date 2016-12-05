// pagination.js
$(document).ready(function() {
    var obj = document.getElementsByClassName('common_name');
    for (i=0;i<obj.length;i++) {
        obj[i].innerHTML = obj[i].innerHTML.split(';')[0];;
    }
});

$(document).ready(function() {
    $('#pagination').DataTable();
});
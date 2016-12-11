// pagination.js
// change common name to display only one name
$(document).ready(function() {
    var obj = document.getElementsByClassName('common_name');
    for (i=0;i<obj.length;i++) {
        obj[i].innerHTML = obj[i].innerHTML.split(';')[0];
    }
});
// change links
$(document).ready(function() {
    var obj = document.getElementsByClassName('species-link');
    for (i=0;i<obj.length;i++) {
        obj[i].href = '/species/' + obj[i].innerHTML.replace(/ /g,'_') + '/'; 
    }
    var obj = document.getElementsByClassName('zoo-link');
    for (i=0;i<obj.length;i++) {
        obj[i].href = '/zoo/' + obj[i].innerHTML.replace(/ /g,'_') + '/'; 
    }
});
// load table after links/names are set
$(document).ready(function() {
    $('#pagination').DataTable();
});
// ensure table is fully loaded before displaying
$(document).ready(function() {
    document.getElementById('pagination').className ='table table-striped table-bordered';
});
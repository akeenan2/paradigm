/* main.js */

$(document).ready(function () {
    $(".navbar-nav li a").click(function(event) {
        $(".navbar-collapse").collapse('hide');
    });
});

$(document).ready(function() { 
    $("table") 
    .tablesorter() 
    .tablesorterPager({container: $("#pager")});
});


(function($) {
    $.extend({
        tablesorterPager: new function() {
            function updatePageDisplay(c) {
                var s = $(c.cssPageDisplay,c.container).val((c.page+1)+c.seperator+c.totalPages);   
            }
            
            function setPageSize(table,size) {
                var c = table.config;
                c.size = size;
                c.totalPages = Math.ceil(c.totalRows/c.size);
                c.pagerPositionSet = false;
                moveToPage(table);
                fixPosition(table);
            }
            function fixPosition(table) {
                var c = table.config;
                if(!c.pagerPositionSet && c.positionFixed) {
                    var c = table.config, o = $(table);
                    if(o.offset) {
                        c.container.css({
                            top: o.offset().top + o.height() + 'px',
                            position: 'absolute'
                        });
                    }
                    c.pagerPositionSet = true;
                }
            }

            function moveToFirstPage(table) {
                var c = table.config;
                c.page = 0;
                moveToPage(table);
            }
            
            function moveToLastPage(table) {
                var c = table.config;
                c.page = (c.totalPages-1);
                moveToPage(table);
            }
            
            function moveToNextPage(table) {
                var c = table.config;
                c.page++;
                if(c.page >= (c.totalPages-1)) {
                    c.page = (c.totalPages-1);
                }
                moveToPage(table);
            }
            
            function moveToPrevPage(table) {
                var c = table.config;
                c.page--;
                if(c.page <= 0) {
                    c.page = 0;
                }
                moveToPage(table);
            }

            function renderTable(table,rows) {
                var c = table.config;
                var l = rows.length;
                var s = (c.page * c.size);
                var e = (s + c.size);
                if(e > rows.length ) {
                    e = rows.length;
                }
                var tableBody = $(table.tBodies[0]);
                // clear the table body
                $.tablesorter.clearTableBody(table);
                
                for(var i = s; i < e; i++) {
                    var o = rows[i];
                    var l = o.length;
                    for(var j=0; j < l; j++) {
                        
                        tableBody[0].appendChild(o[j]);

                    }
                }
                fixPosition(table,tableBody);                
                if(c.page >= c.totalPages) {
                    moveToLastPage(table);
                }
                updatePageDisplay(c);
            }
            this.appender = function(table,rows) {
                var c = table.config;
                c.rowsCopy = rows;
                c.totalRows = rows.length;
                c.totalPages = Math.ceil(c.totalRows / c.size);
                renderTable(table,rows);
            };
            this.defaults = {
                size: 10,
                offset: 0,
                page: 0,
                totalRows: 0,
                totalPages: 0,
                container: null,
                cssNext: '.next',
                cssPrev: '.prev',
                cssFirst: '.first',
                cssLast: '.last',
                cssPageDisplay: '.pagedisplay',
                cssPageSize: '.pagesize',
                seperator: "/",
                positionFixed: true,
                appender: this.appender
            };
            this.construct = function(settings) {
                return this.each(function() {
                    config = $.extend(this.config, $.tablesorterPager.defaults, settings);
                });
            };
        }
    });
    $.fn.extend({
        tablesorterPager: $.tablesorterPager.construct
    });
});

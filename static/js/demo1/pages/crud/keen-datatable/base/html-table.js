"use strict";
// Class definition

var KTDatatableHtmlTableDemo = function() {
    // Private functions

    // demo initializer
    var demo = function() {

        var datatable = $('.kt-datatable').KTDatatable({
            data: {
                saveState: {
                    cookie: false
                },
            },
            layout: {
                scroll: true,
                height: 550,
                footer: false
            },
            
        });

        
    };

    return {
        // Public functions
        init: function() {
            // init dmeo
            demo();
        }
    };
}();

jQuery(document).ready(function() {
    KTDatatableHtmlTableDemo.init();
});
// Call the dataTables jQuery plugin
$(document).ready(function() {
    // DOM-ready auto-init of plugins.
    // Many plugins bind to an "enhance" event to init themselves on dom ready, or when new markup is inserted into the DOM
    // Use raw DOMContentLoaded instead of shoestring (may have issues in Android 2.3, exhibited by stack table)
    // $('.table-responsive').responsiveTable();
    $('.aptinfo-columns').multiselect();
    // (function ($, window) {
    //
    //     new TableExport($('table'), {formats: ['xlsx', 'xls', 'csv', 'txt'], fileName: "contact-list", bootstrap: true})
    //
    // }).call(this, jQuery, window);

});




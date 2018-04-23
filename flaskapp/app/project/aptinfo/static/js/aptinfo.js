(function ($) {
    "use strict"; // Start of use strict    // Shorthand for $( document ).ready()
    $(function() {
        console.log('경고숨기기');
        $(".alert").hide();
    });
    // for aptinfo's search button
    $("#aptInfoSubmitSearchButton").click(function (e) {
        e.preventDefault();
        var values = Sijax.getFormValues('#aptinfo-form-search')
        // alert('다중 조건검색 - 미구현');
        Sijax.request('say_hi',[values])
    });
    $("#aptInfoSearchButton").click(function (e) {
        e.preventDefault();
        // alert('단일 키워드 검색');
        var value = $( "input[name=apt-info-search-keyword]" ).val();
        console.log(value);
        Sijax.request('search_signle', [value]);
    });
})(jQuery); // End of use strict

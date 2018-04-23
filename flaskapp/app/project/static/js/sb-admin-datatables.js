// Call the dataTables jQuery plugin
$(document).ready(function() {
    // DOM-ready auto-init of plugins.
    // Many plugins bind to an "enhance" event to init themselves on dom ready, or when new markup is inserted into the DOM
    // Use raw DOMContentLoaded instead of shoestring (may have issues in Android 2.3, exhibited by stack table)

    TablesawConfig = {
        i18n: {
            modeStack: '쌓기',
            modeSwipe: '넘기기',
            modeToggle: '토글',
            modeSwitchColumnsAbbreviated: '열',
            modeSwitchColumns: '열',
            columnToggleButton: '열',
            columnToggleError: '가능한 열 없음.',
            sort: '정렬',
            swipePreviousColumn: '이전 열',
            swipeNextColumn: '다음 열'
        }
    };

    Tablesaw.init();

});




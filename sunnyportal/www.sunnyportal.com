
<!DOCTYPE html>
<!--[if IE 8]><html class="ie8 oldie"><![endif]-->
<!--[if IE 9 ]><html class="ie9"><![endif]-->
<!--[if gt IE 9]><!--><html><!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        
        <title>PV System List - Koperwiekweg - Sunny Portal</title>
        
        

    <link rel="stylesheet" href="/dist/css/sma.theme.css?v=7.5.21.38096"/>

        

    <link rel="stylesheet" href="/dist/css/sma.modules.css?v=7.5.21.38096"/>


        
    <style>
        
        .dataTable.plantList {
            min-height: 250px;
        }

        .dataTables_wrapper.no-footer {
            margin-bottom: 0;
            min-height: 250px;
        }

        .dataTables_wrapper .fg-toolbar {
            height: auto;
            padding-left: 0px;
        }

        .dataTables_wrapper .fg-toolbar .paging_full_numbers {
            width: auto;
        }
    </style>

        
        

        
<script src="/Scripts/require.js?v=7.5.21.38096"></script>
<script src="/Scripts/requirejs-config.js?v=7.5.21.38096"></script>
<script>
    requirejs.config({ urlArgs: 'v=7.5.21.38096' });
    (function(global, name, factory) {
        global.SMA = global.SMA || {};
        global.SMA[name] = factory();
    }(this, 'version', function() {
        return '7.5.21.38096';
    }));
</script>
        

<script src="/Translation/culture.en-GB.js?v=7.5.21.38096"></script>
<script>
    (function (global, name, factory) {
        global.SMA = global.SMA || {};
        global.SMA[name] = factory();
    }(window || this, 'timezone', function () {
        return {
            standardName: 'W. Europe Standard Time'
        };
    }));
</script>
        
<script>
    (function (global, name, factory) {
        global.SMA = global.SMA || {};
        global.SMA[name] = factory();
    }(window || this, 'translation', function () {
        require(['sma-translation'], function (Translation) {
Translation.add('dataTables', {
                    'Pagination_FirstPage': 'First page',
                    'Pagination_LastPage': 'Last page',
                    'Pagination_NextPage': 'Next page',
                    'Pagination_PrevPage': 'Previous page',
                    'NoData': 'No data',
                    'ASA_UserPlantList_Datatable_sInfo': '_START_ to _END_ of _TOTAL_ entries',
                    'ASA_UserPlantList_Datatable_sInfoFiltered': ' (filtered from a total of _MAX_ entries)',
                    'ASA_UserPlantList_Datatable_sLengthMenu': 'Show _MENU_ entries',
                    'Mode_loading': 'Loading...',
                    'search': 'Search',
                    'ASA_UserPlantList_Datatable_plugins_ColVis_buttonText': 'Hide/show columns',
                    'sort_descending_title': 'Sort in descending order',
                    'sort_ascending_title': 'Sort in ascending order',
                    'ShowHideColumns': 'Hide / show columns',
                });
Translation.add('datePicker', {
                    'closeText': 'Close',
                    'prevText': 'Back',
                    'nextText': 'Next',
                    'currentText': 'Today',
                    'yearSuffix': 'Year',
                });
Translation.add('colorPicker', {
                    'cancelText': 'Cancel',
                    'chooseText': 'Select',
                    'clearText': 'Clear color selection',
                    'noColorSelectedText': 'No color selected',
                    'togglePaletteMoreText': 'More',
                    'togglePaletteLessText': 'Less',
                });
Translation.add('intro', {
                    'nextLabel': 'Next',
                    'prevLabel': 'Back',
                    'skipLabel': 'Close',
                    'doneLabel': 'Close',
                });
Translation.add('areYouSure', {
                    'message': 'You have unsaved changes.',
                    'NotSupportedBrowser': 'This function is currently not available when using the browser {0}. Please use an alternative browser.',
                });
Translation.add('validation', {
                    'error_required': 'The field "{0}" is required.',
                    'error_string_max_length': 'The field "{0}" may contain a maximum of {1} characters.',
                    'error_invalid_company_tax_id': 'The entry in the field "Company VAT number" is invalid.',
                    'validation_number': 'Enter a valid number.',
                });
        });
    }));
</script>
         

<script>
    (function (global, name, factory) {
        global.SMA = global.SMA || {};
        global.SMA[name] = factory();
    }(window || this, 'user', function () {
        return {
            checkoutid: 'cda7d7bf-0497-4752-bb96-bddf8d047ff6',
            userid: '018171fc-3b66-4b8a-98d3-f621bd64f4cc'
        };
    }));
</script>
            <script src="/dist/js/sma.scripts.min.js?v=7.5.21.38096"></script>
    <script src="/dist/js/sma.webmodules.min.js?v=7.5.21.38096"></script>
    <script src="/dist/js/sma.sp.min.js?v=7.5.21.38096"></script>

<script>
    require(['sp-init-main'], function (sp) {
        sp.init();
    });
</script>
    </head>
    <body class="naviHidden" data-lang="en-GB" data-layout="Default">
            <div id="DivOpac50BG" style="z-Index: 9999;"></div>

<div class="header collapsible " style="z-index: 11">
    <h1 class="portalName header"><a href="/Home">SUNNY PORTAL</a></h1>
    <!-- group left header nav -->
    <ul class="headerNav">
        <li class="hasChildren last">
            <a href="#">English</a>
            <ul class="headerNavSubLevel twoColumn css3pie">
                <li class="first"><a href="#">English</a></li>
                        <li><a id="lang_de-de" href="/Language/SetLanguage/de-de" 
                            class="lang_de-de">Deutsch</a></li>
                        <li><a id="lang_en-us" href="/Language/SetLanguage/en-us" 
                            class="lang_en-us">US-English</a></li>
                        <li><a id="lang_it-it" href="/Language/SetLanguage/it-it" 
                            class="lang_it-it">Italiano</a></li>
                        <li><a id="lang_es-es" href="/Language/SetLanguage/es-es" 
                            class="lang_es-es">Espa&#241;ol</a></li>
                        <li><a id="lang_fr-fr" href="/Language/SetLanguage/fr-fr" 
                            class="lang_fr-fr">Fran&#231;ais</a></li>
                        <li><a id="lang_ko-kr" href="/Language/SetLanguage/ko-kr" 
                            class="lang_ko-kr">한국어</a></li>
                        <li><a id="lang_cs-cz" href="/Language/SetLanguage/cs-cz" 
                            class="lang_cs-cz">Čeština</a></li>
                        <li><a id="lang_zh-cn" href="/Language/SetLanguage/zh-cn" 
                            class="lang_zh-cn">中文</a></li>
                        <li><a id="lang_el-gr" href="/Language/SetLanguage/el-gr" 
                            class="lang_el-gr">Ελληνικά</a></li>
                        <li><a id="lang_pt-pt" href="/Language/SetLanguage/pt-pt" 
                            class="lang_pt-pt">Portugu&#234;s</a></li>
                        <li><a id="lang_nl-nl" href="/Language/SetLanguage/nl-nl" 
                            class="lang_nl-nl">Nederlands</a></li>
                        <li><a id="lang_ja-jp" href="/Language/SetLanguage/ja-jp" 
                            class="lang_ja-jp">日本語</a></li>
                        <li><a id="lang_tr-tr" href="/Language/SetLanguage/tr-tr" 
                            class="lang_tr-tr">T&#252;rk&#231;e</a></li>
            </ul>
        </li>
    </ul>
    <!-- end left header nav -->


    <!-- group right header nav -->
        <ul class="headerNav right">
                            <li class="user hasChildren last">
                    <a href="#">Henk van Veluw</a>
                    <ul class="headerNavSubLevel css3pie" style="z-index: 100">
                        <li class="first"><a href="#">Henk van Veluw</a></li>
 <li><a href="/Templates/UserProfile.aspx">Personal data</a></li>                          <li><a href="/Templates/UserSettings.aspx">Preferred base units</a></li>                          <li class="logout"><a href="/Templates/Logout.aspx">Logout</a></li>                     </ul>
                </li>
        </ul>
    <!-- end right header nav -->

    <!--group Toolbar -->
    <div id="toolbar">
        <ul id="rightTopNav">
                    </ul>
    </div>
    <!--end Toolbar -->
</div>

<div id="headerSeparator">
    <a href="#" id="collapseHeader" ></a>
</div>
            <div class="page-wrapper clearfix">
                <div id="content" class=" contentFull  ignoreNaviCookie">
                    

<div class="notabs contentCoat pageBloat">

    <h2 class="header">PV System List</h2>

    <table class="dataTable plantList"></table>

    <div class="text-right">
        <a href="/Plants/Download" title="Download">
            <img src="/Images/download.png" alt="Download" />
        </a>
    </div>
</div>



                </div>
            </div>
            <div id="statusbar">
                <span id="statusbarLoading">
                    <img src="/Images/loading.gif" width="62" height="23" alt="Loading">
                </span>
                
                <div id="StickyFooter" class="FooterClass" style="margin-bottom:-31px; font-size:11px; border:none;">
    <span id="statusbarDesc">© 2015 SMA Solar Technology AG
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="/Home" class="footerLink">Home</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="/RedirectToPage/INFO" class="footerLink" target="_blank">Information</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="/RedirectToPage/MANUALS_HOMAN" class="footerLink" target="_blank">User manuals</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;   

        <a href="https://www.sma.de/en/service/faq-support.html" class="footerLink" target="_blank">FAQ</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="/RedirectToPage/TERMS_AND_CONDITIONS" class="footerLink" target="_blank">Terms of Use</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="/RedirectToPage/DATA_PROTECTION_DECLARATION" class="footerLink" target="_blank">Data protection declaration</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="/RedirectToPage/CONTACT" class="footerLink" target="_blank">Legal Notice</a>
    </span>
</div>

            </div>

        
        <script src="/dist/js/sma.plants.min.js?v=7.5.21.38096"></script>
    <script>
        require(['plants-list'], function(main) {
            main.init(1, 50, 6, 'asc');
        });
    </script>

        
        

<script type="text/javascript">
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-839066-23']);
    _gaq.push(['_trackPageview']);

    (function () {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
</script>
    </body>
</html>
 
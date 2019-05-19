function get_search_ref()
    {
        var smp_t = document.getElementById("SimpleType").options.selectedIndex;
        var clr_t = document.getElementById("ColorsType").options.selectedIndex;
        var stn_t = document.getElementById("StoneType").options.selectedIndex;
        var mgchr_t = document.getElementById("MagCharType").options.selectedIndex;
        var mdchr_t = document.getElementById("MedCharType").options.selectedIndex;
        var price_from = document.getElementById("PriceFrom").value;
        var price_to = document.getElementById("PriceTo").value;
        var request_str = document.getElementById("NameType").value;

        document.getElementById('SearchButton').href = '/search' + '?q=' + request_str + '&tags=' + smp_t + ',' +
                                clr_t + ',' + stn_t + ',' + mgchr_t + ',' + mdchr_t + '&price=' + price_from + ',' +
                                price_to;
    }

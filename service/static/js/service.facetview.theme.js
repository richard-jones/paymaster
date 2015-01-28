jQuery(document).ready(function($) {

    /****************************************************************
     * Application Facetview Theme
     *****************************
     */

    function customFacetview(options) {
        /*****************************************
         * overrides must provide the following classes and ids
         *
         * id: facetview - main div in which the facetview functionality goes
         * id: facetview_filters - div where the facet filters will be displayed
         * id: facetview_rightcol - the main window for result display (doesn't have to be on the right)
         * class: facetview_search_options_container - where the search bar and main controls will go
         * id : facetview_selectedfilters - where we summarise the filters which have been selected
         * class: facetview_metadata - where we want paging to go
         * id: facetview_results - the table id for where the results actually go
         * id: facetview_searching - where the loading notification can go
         *
         * Should respect the following configs
         *
         * options.debug - is this a debug enabled facetview.  If so, put a debug textarea somewhere
         */

        // the facet view object to be appended to the page
        var thefacetview = '<div id="facetview"><div class="row">';

        // if there are facets, give them span3 to exist, otherwise, take up all the space
        var showfacets = false;
        for (var i = 0; i < options.facets.length; i++) {
            var f = options.facets[i];
            if (!f.hidden) {
                showfacets = true;
                break;
            }
        }
        if (showfacets) {
            thefacetview += '<div class="col-md-3"><div id="facetview_filters" style="padding-top:45px;"></div></div>';
            thefacetview += '<div class="col-md-9" id="facetview_rightcol">';
        } else {
            thefacetview += '<div class="col-md-12" id="facetview_rightcol">';
        }

        // make space for the search options container at the top
        thefacetview += '<div class="facetview_search_options_container"></div>';

        // make space for the selected filters
        thefacetview += '<div style="margin-top: 20px"><div class="row"><div class="col-md-12"><div class="btn-toolbar" id="facetview_selectedfilters"></div></div></div></div>';

        // make space at the top for the pager
        thefacetview += '<div class="facetview_metadata" style="margin-top:20px;"></div>';

        // insert loading notification
        thefacetview += '<div class="facetview_searching" style="display:none"></div>'

        // insert the table within which the results actually will go
        thefacetview += '<div class="row">';
        thefacetview += "<div class='col-md-1'>Ref</div>";
        thefacetview += "<div class='col-md-1'>Invoice Date</div>";
        thefacetview += "<div class='col-md-1'>Incoming</div>";
        thefacetview += "<div class='col-md-1'>VAT</div>";
        thefacetview += "<div class='col-md-1'>Overhead</div>";
        thefacetview += "<div class='col-md-1'>Expenses</div>";
        thefacetview += "<div class='col-md-1'>Available</div>";
        thefacetview += "<div class='col-md-1'>Central Costs</div>";
        thefacetview += "<div class='col-md-3'>Shares</div>";
        thefacetview += "<div class='col-md-1'></div>";
        thefacetview += '</div>';
        thefacetview += '<div id="facetview_results"></div>';

        // make space at the bottom for the pager
        thefacetview += '<div class="facetview_metadata"></div>';

        // debug window near the bottom
        if (options.debug) {
            thefacetview += '<div class="facetview_debug" style="display:none"><textarea style="width: 95%; height: 300px"></textarea></div>'
        }

        // close off all the big containers and return
        thefacetview += '</div></div></div>';
        return thefacetview
    }

    var status_colour = {
        "not_estimated" : "C4C4C4",
        "estimated" : "4545FF",
        "not_invoiced" : "FF1FD2",
        "invoiced" : "FF2E1F",
        "paid_to_cl" : "FFA91F",
        "requested" :"F9FF4A",
        "paid_to_me" : "00FF1E"
    };

    function discoveryRecordView(options, record) {

        var payment = octopus.service.newPayment({raw : record});

        var ref = payment.get_field("ref");
        var date = payment.get_field("invoice_date");
        if (!date) { date = "" }
        var amount = payment.amount();
        var vat = payment.get_field("vat");
        var overhead = payment.get_field("overhead");
        var expenses = payment.total_expenses();
        var available = payment.get_field("available");
        var shares = payment.share_summary();
        var central = payment.total_central();
        var state = payment.get_field("state");

        var partners = Object.keys(shares);
        var report = "";
        for (var i = 0; i < partners.length; i++) {
            var p = partners[i];
            if (i > 0) { report += " " }
            report += p + ": " + shares[p].total;
        }

        var colour = status_colour[state];

        // var result = options.resultwrap_start;
        var result = "";
        result += "<div class='row'>";
        result += "<div class='col-md-12'>";
        result += "<div class='row' style='background: #" + colour + "'>";

        result += "<div class='col-md-1'>" + ref + "</div>";
        result += "<div class='col-md-1'>" + date + "</div>";
        result += "<div class='col-md-1'>" + amount + "</div>";
        result += "<div class='col-md-1'>" + vat + "</div>";
        result += "<div class='col-md-1'>" + overhead + "</div>";
        result += "<div class='col-md-1'>" + expenses + "</div>";
        result += "<div class='col-md-1'>" + available + "</div>";
        result += "<div class='col-md-1'>" + central + "</div>";
        result += "<div class='col-md-3'>" + report + "</div>";
        result += "<div class='col-md-1'><a href='#' class='edit_link' data-id='" + payment.get_field("id") + "'>more</a></div>";

        result += "</div>";

        result += "<div class='row' style='display:none' id='edit_" + payment.get_field("id") + "'><div class='col-md-12'>a form</div></div>";

        result += "</div></div>";
        // result += options.resultwrap_end;
        return result;
    }

    function postRender(options, context) {
        $(".edit_link", context).unbind("click");
        $(".edit_link", context).click(function(event) {
            event.preventDefault();
            var id = $(this).attr("data-id");
            octopus.fragments.frag({id : "payment_form", callback: renderFormClosure(id, context)});
        })
    }

    function renderFormClosure(id, context) {
        function renderForm(html) {
            var editid = '#edit_' + id;
            $(editid).find("div").html(html);
            $(editid, context).slideToggle();
        }
        return renderForm
    }


    var facets = [];
    facets.push({'field' : 'state.exact', 'display' : 'State', 'open' : true});
    facets.push({'field' : 'shares.who.exact', 'display' : 'Partner', 'open' : true});

    $('#payments_facetview').facetview({
        debug: false,
        search_url : octopus.config.payment_query_endpoint,
        page_size : 100,
        facets : facets,
        search_sortby : [
            {'display':'Last Modified','field':'last_updated'},
            {'display':'Date Created','field':'created_date'}
        ],
        searchbox_fieldselect : [
            {'display':'ID','field':'id'}
        ],
        render_result_record : discoveryRecordView,
        render_the_facetview : customFacetview,
        sort : [{"created_date" : {"order" : "desc"}}],
        post_render_callback : postRender
    });

});

jQuery(document).ready(function($) {
    $.extend(octopus, {
        service : {

            newPayment : function() {
                return octopus.dataobj.newDataObj({
                    schema : {
                        ref : {
                            type : "single",
                            path : "ref",
                            coerce : String
                        }
                    }

                });
            }

        }
    });
});

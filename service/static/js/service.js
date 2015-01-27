jQuery(document).ready(function($) {
    $.extend(octopus, {
        page : {

        },

        service : {

            newPayment : function(params) {
                var schema = {
                    id : {type : "single", path : "id", coerce: String },
                    created_date : {type : "single", path : "created_date", coerce: String},
                    last_updated : {type : "single", path : "last_updated", coerce: String},

                    ref : { type : "single", path : "ref", coerce : String},
                    description : { type : "single", path : "description", coerce : String },
                    invoice_date : { type : "single", path : "invoice", coerce: String },
                    expected_amount : { type : "single", path : "expected_amount", coerce: parseFloat},
                    actual_amount : { type: "single", path : "actual_amount", coerce: parseFloat },
                    vat_pc : { type: "single", path : "vat_pc", coerce: parseFloat },
                    vat : { type: "single", path : "vat", coerce: parseFloat },
                    overhead_pc : { type: "single", path : "overhead_pc", coerce: parseFloat },
                    overhead : { type: "single", path : "overhead", coerce: parseFloat },
                    available : { type: "single", path : "available", coerce: parseFloat },
                    notes : { type: "single", path : "notes", coerce: String },
                    state : { type: "single", path : "state", coerce: String,
                        allowed_values: ["not_estimated", "estimated", "not_invoiced", "invoiced", "paid_to_cl", "requested", "paid_to_me"]
                    },
                    expenses : { type: "list", path : "expenses",
                        coerce: function(obj) {
                            if (obj.ref) { obj.ref = String(obj.ref) }
                            if (obj.amount) { obj.amount = parseFloat(obj.amount) }
                            if (obj.allocate_to) { obj.allocate_to = String(obj.allocate_to) }
                            return obj;
                        }
                    },
                    shares : {type : "list", path: "shares",
                        coerce: function(obj) {
                            if (obj.who) { obj.who = String(obj.who) }
                            if (obj.pc) { obj.pc = parseFloat(obj.pc) }
                            if (obj.share_amount) { obj.share_amount = parseFloat(obj.share_amount) }
                            if (obj.expenses) { obj.expenses = parseFloat(obj.expenses) }
                            if (obj.total) { obj.total = parseFloat(obj.total) }
                            return obj;
                        }
                    },
                    central : {type: "list", path: "central",
                        coerce : function(obj) {
                            if (obj.ref) { obj.ref = String(obj.ref) }
                            if (obj.description) { obj.description = String(obj.description) }
                            if (obj.amount) { obj.amount = parseFloat(obj.amount) }
                            return obj;
                        }
                    }
                };

                var Payment = function() {
                    this.data = {};
                    this.schema = {};
                    this.allow_off_schema = false;
                };

                var proto = $.extend(octopus.dataobj.DataObjPrototype, octopus.service.PaymentPrototype);
                Payment.prototype = proto;

                var dobj = new Payment();
                dobj.schema = schema;
                if (params) {
                    if (params.raw) {
                        dobj.data = params.raw;
                    }
                }
                return dobj;
            },

            PaymentPrototype : {
                amount : function() {
                    var actual = this.get_field("actual_amount");
                    if (actual) { return actual }
                    return this.get_field("expected_amount");
                },

                total_expenses : function() {
                    var expenses = this.get_field("expenses");
                    var tot = 0;
                    for (var i = 0; i < expenses.length; i++) {
                        tot += expenses[i].amount;
                    }
                    return tot;
                },

                share_summary : function() {
                    var shares = this.get_field("shares");
                    var summary = {};
                    for (var i = 0; i < shares.length; i++) {
                        summary[shares[i].who] = shares[i];
                    }
                    return summary;
                },

                total_central : function() {
                    var central = this.get_field("central");
                    var tot = 0;
                    for (var i = 0; i < central.length; i++) {
                        tot += central[i].amount;
                    }
                    return tot;
                }
            },

            calculate : function(payment) {

                function round2dp(n) {
                    return Math.round(n * 100)/100;
                }

                // get all the numbers that we want to work with
                var incoming = payment.get_field("actual_amount") ? payment.get_field("actual_amount") : payment.get_field("expected_amount");
                if (!incoming) { incoming = 0 }

                var vat_pc = payment.get_field("vat_pc") ? payment.get_field("vat_pc") : 0;

                var overhead_pc = payment.get_field("overhead_pc") ? payment.get_field("overhead_pc") : 0;

                // calculate the VAT and overheads, giving us the spendable amount
                var vat = incoming - (incoming / (1.0 + (vat_pc / 100)));
                vat = round2dp(vat);
                payment.set_field("vat", vat);

                var lessvat = incoming - vat;

                var overhead = round2dp((overhead_pc / 100) * lessvat);
                payment.set_field("overhead", overhead);

                var spendable = lessvat - overhead;

                // calculate the total expenses, and the available amount, and record the expense allocations
                var expenses = payment.get_field("expenses");
                var total_expenses = 0;
                var allocations = {};
                if (expenses) {
                    for (var i = 0; i < expenses.length; i++) {
                        var expense = expenses[i];
                        if (expense.amount) {
                            total_expenses += expense.amount;
                            if (expense.allocate_to) {
                                if (allocations.hasOwnProperty(expense.allocate_to)) {
                                    allocations[expense.allocate_to] += expense.amount;
                                } else {
                                    allocations[expense.allocate_to] = expense.amount;
                                }
                            }

                        }
                    }
                }

                var available = round2dp(spendable - total_expenses);
                payment.set_field("available", available);

                // deduct the central costs to get the shareable amount
                var central = payment.get_field("central");
                var total_central = 0;
                if (central) {
                    for (i = 0; i < central.length; i++) {
                        var c = central[i];
                        if (c.amount) {
                            total_central += c.amount;
                        }
                    }
                }

                var shareable = available - total_central;

                // now calculate each of the partner shares
                var partners = payment.get_field("shares");
                if (partners) {
                    for (i = 0; i < partners.length; i++) {
                        var p = partners[i];
                        var share_pc = p.pc ? p.pc : 0;
                        var share = round2dp((share_pc / 100) * shareable);
                        p.share_amount = share;
                        p.total = p.share_amount;
                        if (allocations.hasOwnProperty(p.who)) {
                            p.expenses = allocations[p.who];
                            p.total += p.expenses;
                        }
                    }
                }
            },

            formFrag : function(params) {
                var callback = params.callback;
                $.ajax({
                    type: "GET",
                    dataType: "html",
                    url: octopus.config.fragments_endpoint + "/payment_form",
                    success: callback
                })
            }
        }
    });
});

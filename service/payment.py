from wtforms import Form, StringField, TextAreaField, DateField, FloatField, SelectField, validators, FieldList, FormField
from octopus.modules.form.validate import DataOptional
from octopus.modules.form.context import FormContext, Renderer

# All the form definitions
##############################################################################################

STATES = [("paid_to_me", "Paid to me"), ("requested", "Requested"), ("paid_to_cl", "Paid to CL"),
          ("invoiced", "Invoiced"), ("not_invoiced", "Not Invoiced"), ("estimated", "Estimated"),
          ("not_estimated", "Not Estimated")]

class Expenses(Form):
    ref = StringField("Expense Reference", [validators.DataRequired()])
    amount = FloatField("Expense Amount", [validators.DataRequired()])
    allocate_to = StringField("Allocate To", [DataOptional()])

class Shares(Form):
    who = StringField("Partner", [validators.DataRequired()])
    pc = FloatField("Share %", [validators.DataRequired()])
    share_amount = FloatField("Share Amount", [validators.DataRequired()])
    expenses = FloatField("Expenses", [DataOptional()])
    total = FloatField("Total Due", [validators.DataRequired()])

class Central(Form):
    ref = StringField("Central Cost Reference", [validators.DataRequired()])
    description = TextAreaField("Cost Description", [DataOptional()])
    amount = FloatField("Total Due", [validators.DataRequired()])

class PaymentForm(Form):
    ref = StringField("Payment Reference", [validators.DataRequired()])
    description = TextAreaField("Description", [DataOptional()])
    invoice_date = DateField("Invoice Date", [DataOptional()])
    expected_amount = FloatField("Expected Amount", [validators.DataRequired()])
    actual_amount = FloatField("Actual Amount", [DataOptional()])
    vat_pc = FloatField("VAT %", [DataOptional()])
    vat = FloatField("VAT Charges", [DataOptional()])
    overhead_pc = FloatField("Overhead %", [DataOptional()])
    overhead = FloatField("Overhead", [DataOptional()])
    available = FloatField("Available", [DataOptional()])
    notes = TextAreaField("Notes", [DataOptional()])
    state = SelectField("State", [validators.DataRequired()], choices=STATES)

    expenses = FieldList(FormField(Expenses), min_entries=1)
    shares = FieldList(FormField(Shares), min_entries=1)
    central = FieldList(FormField(Central), min_entries=1)

# The form context
#################################################################################################

class PaymentFormContext(FormContext):
    def make_renderer(self):
        """
        This will be called during init, and must populate the self.render property
        """
        self.renderer = PaymentRenderer()

    def set_template(self):
        """
        This will be called during init, and must populate the self.template property with the path to the jinja template
        """
        self.template = "payment_form.html"

    def pre_validate(self):
        """
        This will be run before validation against the form is run.
        Use it to patch the form with any relevant data, such as fields which were disabled
        """
        pass

    def blank_form(self):
        """
        This will be called during init, and must populate the self.form property with an instance of the form in this
        context, based on no originating source or form_data
        """
        self.form = PaymentForm()

    def data2form(self):
        """
        This will be called during init, and must convert the self.form_data into an instance of the form in this context,
        and write to self.form
        """
        self.form = PaymentForm(formdata=self.form_data)

    def source2form(self):
        """
        This will be called during init, and must convert the source object into an instance of the form in this
        context, and write to self.form
        """
        pass

    def form2target(self):
        """
        Convert the form object into a the target system object, and write to self.target
        """
        pass

    def patch_target(self):
        """
        Patch the target with data from the source.  This will be run by the finalise method (unless you override it)
        """
        pass

class PaymentRenderer(Renderer):
    def __init__(self):
        super(PaymentRenderer, self).__init__()

        self.FIELD_GROUPS = {
            "basic_info" : {
                "helper" : "bs3_horizontal",
                "wrappers" : [],
                "label_width" : 4,
                "control_width" : 8,
                "fields" : [
                    {"ref" : {}},
                    {"state" : {}},
                    {"description" : {}},
                    {"invoice_date" : {}},
                    {"expected_amount" : {"attributes" : {"class" : "input-small"}}},
                    {"actual_amount" : {"attributes" : {"class" : "input-small"}}},
                    {"vat_pc" : {"attributes" : {"class" : "input-small"}}},
                    {"vat" : {"attributes" : {"class" : "input-small"}}},
                    {"overhead_pc" : {"attributes" : {"class" : "input-small"}}},
                    {"overhead" : {"attributes" : {"class" : "input-small"}}},
                    {"notes" : {}}
                ]
            },
            "expenses" : {
                "helper" : "bs3_horizontal",
                "wrappers" : [],
                "label_width" : 4,
                "control_width" : 8,
                "fields" : [
                    {
                        "expenses" : {
                            "fields" : [
                                {"ref" : {}},
                                {"amount" : {"attributes" : {"class" : "input-small"}}},
                                {"allocate_to" : {}}
                            ]
                        }
                    }
                ]
            },
            "shares" : {
                "helper" : "bs3_horizontal",
                "wrappers" : [],
                "label_width" : 4,
                "control_width" : 8,
                "fields" : [
                    {
                        "shares" : {
                            "fields" : [
                                {"who" : {}},
                                {"pc" : {"attributes" : {"class" : "input-small"}}},
                                {"share_amount" : {"attributes" : {"class" : "input-small"}}},
                                {"expenses" : {"attributes" : {"class" : "input-small"}}},
                                {"total" : {"attributes" : {"class" : "input-small"}}},
                            ]
                        }
                    }
                ]
            },
            "central" : {
                "helper" : "bs3_horizontal",
                "wrappers" : [],
                "label_width" : 4,
                "control_width" : 8,
                "fields" : [
                    {
                        "central" : {
                            "fields" : [
                                {"ref" : {}},
                                {"description" : {}},
                                {"amount" : {"attributes" : {"class" : "input-small"}}}
                            ]
                        }
                    }
                ]
            },
            "total" : {
                "helper" : "bs3_horizontal",
                "wrappers" : [],
                "label_width" : 4,
                "control_width" : 8,
                "fields" : [
                    {"available" : {}}
                ]
            }
        }


        """
        self.FIELD_GROUPS = {
            "basic_info" : [
                {"ref" : {"class" : "form-control"}},
                {"state" : {"class": "form-control"}},
                {"description" : {"class" : "form-control"}},
                {"invoice_date" : {"class" : "form-control"}},
                {"expected_amount" : {"class" : "form-control input-small"}},
                {"actual_amount" : {"class" : "form-control input-small"}},
                {"vat_pc" : {"class" : "form-control input-small"}},
                {"vat" : {"class" : "form-control input-small"}},
                {"overhead_pc" : {"class" : "form-control input-small"}},
                {"overhead" : {"class" : "form-control input-small"}},
                {"notes" : {"class" : "form-control"}}
            ],
            "expenses" : [
                {"expenses" : {"class" : "form-control"}},
            ],
            "shares" : [
                {"shares" : {}}
            ],
            "central" : [
                {"central" : {}}
            ],
            "total" : [
                {"available" : {}}
            ]
        }
        """
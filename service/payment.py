from wtforms import Form, StringField, TextAreaField, DateField, FloatField, SelectField, validators, FieldList, FormField
from octopus.modules.form.validate import DataOptional
from octopus.modules.form.context import FormContext, Renderer
from octopus.core import app

# All the form definitions
##############################################################################################

STATES = [("not_estimated", "Not Estimated"), ("estimated", "Estimated"), ("not_invoiced", "Not Invoiced"),
          ("invoiced", "Invoiced"), ("paid_to_cl", "Paid to CL"), ("requested", "Requested"),
          ("paid_to_me", "Paid to me")]

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
    vat_pc = FloatField("VAT %", [DataOptional()], default=app.config.get("DEFAULT_VAT_PC"))
    vat = FloatField("VAT Charges", [DataOptional()])
    overhead_pc = FloatField("Overhead %", [DataOptional()], default=app.config.get("DEFAULT_OVERHEAD_PC"))
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
                    {"ref" : {"attributes" : {"data-parsley-required" : "true"}}},
                    {"state" : {}},
                    {"description" : {}},
                    {"invoice_date" : {}},
                    {"expected_amount" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}},
                    {"actual_amount" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}},
                    {"vat_pc" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}},
                    {"vat" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "disabled" : "disabled"}}},
                    {"overhead_pc" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}},
                    {"overhead" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "disabled" : "disabled"}}},
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
                                {"amount" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}},
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
                                {"pc" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}},
                                {"share_amount" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "disabled" : "disabled"}}},
                                {"expenses" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "disabled" : "disabled"}}},
                                {"total" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "disabled" : "disabled"}}},
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
                                {"amount" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "data-parsley-group" : "calculate"}}}
                            ]
                        }
                    }
                ]
            },
            "total" : {
                "helper" : "bs3_horizontal",
                "wrappers" : [],
                "label_width" : 2,
                "control_width" : 10,
                "fields" : [
                    {"available" : {"attributes" : {"class" : "input-small", "data-parsley-type" : "number", "disabled" : "disabled"}}}
                ]
            }
        }
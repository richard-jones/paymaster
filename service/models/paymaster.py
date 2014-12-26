from octopus.lib import dataobj
from service import dao
from octopus.modules.crud.models import ES_CRUD_Wrapper

class Payment(dataobj.DataObj, dao.PaymentDAO):
    """
    {
        "id" : "<opaque id for object>",
        "crated_date" : "<date record created>",
        "last_updated" : "<date record last modified>",

        "ref" : "<payment reference (e.g. invoice number)",
        "description" : "<additional descriptive information if necessary>",
        "invoice_date" : "<date invoice should be/was sent>",
        "expected_amount" : <how much is expected to be paid>,
        "actual_amount" : <how much was actually paid>,
        "vat_pc" : <rate VAT was charged at>,
        "vat" : <total VAT as part of payment>,
        "overhead_pc" : <rate overhead charged at>,
        "overhead" : <total overhead as part of payment>,
        "available" : <total available for partner shares>,
        "notes" : "<freetext notes field>",
        "state" : "<workflow state: paid_to_me|requested|paid_to_cl|invoiced|not_invoiced|estimated|not_estimated>",

        "expenses" : [
            {
                "ref" : "<expense reference>",
                "amount" : <total expense>,
                "allocate_to" : "<partner id in shares section>"
            }
        ],
        "shares" : [
            {
                "who" : "<partner id receiving share>",
                "pc" : <% share by this partner>,
                "share_amount" : <share of available funds>,
                "expenses" : <total amount of expenses due>,
                "total" : <total due>
            }
        ],
        "central" : [
            {
                "ref" : "<key word for type of central cost, e.g. staff, sysadmin>",
                "description" : "<description of contribution to central>",
                "amount" : <total contribution>
            }
        ]
    }
    """
    SCHEMA = {
        "fields" : [
            "id", "created_date", "last_updated", "ref", "description", "invoice_date", "expected_amount", "actual_amount",
            "vat_pc", "vat", "overhead_pc", "overhead", "available", "notes", "state"
        ],
        "lists" : ["expenses", "shares", "central"],
        "list_entries" : {
            "expenses" : {
                "fields" : ["ref", "amount", "allocate_to"]
            },
            "shares" : {
                "fields" : ["who", "pc", "share_amount", "expenses", "total"]
            },
            "central" : {
                "fields" : ["ref", "description", "amount"]
            }
        }
    }

class CRUDPayment(ES_CRUD_Wrapper):
    INNER_TYPE = Payment

    def __init__(self, raw=None):
        if raw is not None:
            # remove any disallowed fields
            if "id" in raw:
                del raw["id"]
            if "created_date" in raw:
                del raw["created_date"]
            if "last_updated" in raw:
                del raw["last_updated"]

        super(CRUDPayment, self).__init__(raw)

    def update(self, data):
        # carry over the data from the old object
        data["id"] = self.inner.id
        data["created_date"] = self.inner.created_date

        # remove any disallowed fields
        if "last_updated" in data:
            del data["last_updated"]

        super(CRUDPayment, self).update(data)
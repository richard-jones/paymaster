# Paymaster

## Data Model

```python
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
```
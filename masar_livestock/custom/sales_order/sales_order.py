import frappe
from frappe.utils import flt, cint


def validate(doc, method):
    validate_livestock_items(doc)


def validate_livestock_items(doc):
    for row in doc.items:
        if not row.item_code:
            continue

        item = frappe.get_doc("Item", row.item_code)

        if not item.custom_is_livestock:
            row.custom_headcount = None
            row.custom_weight_kg = None
            continue

        if not row.custom_headcount or row.custom_headcount <= 0:
            frappe.throw(
                f"Headcount must be greater than zero "
                f"for livestock item {row.item_code} in row {row.idx}"
            )

        if not row.custom_weight_kg or row.custom_weight_kg <= 0:
            frappe.throw(
                f"Weight (Kg) must be greater than zero "
                f"for livestock item {row.item_code} in row {row.idx}"
            )

        headcount = cint(row.custom_headcount)
        weight = flt(row.custom_weight_kg)

        row.uom = "Nos"
        row.qty = headcount

        conversion_factor = flt(weight / headcount, 9)


        row.conversion_factor = conversion_factor
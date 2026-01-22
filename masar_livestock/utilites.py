import frappe
from frappe.utils import flt, cint


def validate_livestock_items(self):
    for row in self.items:
        item = frappe.get_doc("Item", row.item_code)

        if not item.custom_is_livestock:
            row.custom_headcount = None
            row.custom_weight_per_unit = None
            continue

        if not row.custom_headcount or row.custom_headcount <= 0:
            frappe.throw(
                f"Headcount must be greater than zero "
                f"for livestock item {row.item_code} in row {row.idx}"
            )

        headcount = cint(row.custom_headcount)

        weight_per_unit = flt(row.qty / headcount)

        row.custom_weight_per_unit = weight_per_unit
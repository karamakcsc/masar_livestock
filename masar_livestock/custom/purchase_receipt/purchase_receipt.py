import frappe
from frappe.utils import flt, cint


def validate(self, method):
    validate_livestock_items(self)
def on_submit(self, method):
    update_batch(self)


def validate_livestock_items(self):
    for row in self.items:
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

def update_batch(self):
    for item in self.items:
        item_doc = frappe.get_doc("Item", item.item_code)
        if item_doc.custom_is_livestock:
            if item.serial_and_batch_bundle:
                sabb_doc = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)
                if sabb_doc.entries:
                    for entry in sabb_doc.entries:
                        if entry.batch_no:
                            batch_doc = frappe.get_doc("Batch", entry.batch_no)
                            batch_doc.custom_current_headcount = item.custom_headcount
                            batch_doc.save(ignore_permissions=True)
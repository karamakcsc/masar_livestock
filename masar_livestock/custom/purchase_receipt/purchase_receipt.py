import frappe
from masar_livestock.utilites import validate_livestock_items


def validate(self, method):
    validate_livestock_items(self)
def on_submit(self, method):
    update_batch(self)


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
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

def set_headcount_sle_sabb(self):
    sles = frappe.get_all(
        "Stock Ledger Entry",
        filters={
            "voucher_type": self.doctype,
            "voucher_no": self.name,
        },
        fields=[
            "name",
            "voucher_detail_no",
            "actual_qty",
            "serial_and_batch_bundle",
        ]
    )

    sle_by_row = {}
    for sle in sles:
        sle_by_row.setdefault(sle.voucher_detail_no, []).append(sle)

    for row in self.items:
        if not row.custom_headcount:
            continue

        item = frappe.get_doc("Item", row.item_code)
        if not item.custom_is_livestock:
            continue

        for sle in sle_by_row.get(row.name, []):
            signed_headcount = (
                row.custom_headcount
                if sle.actual_qty > 0
                else -row.custom_headcount
            )

            frappe.db.set_value(
                "Stock Ledger Entry",
                sle.name,
                "custom_headcount",
                signed_headcount
            )

            if sle.serial_and_batch_bundle:
                update_sabb_and_batches(
                    sle.serial_and_batch_bundle,
                    row.custom_weight_per_unit
                )

def reverse_headcount_sle_sabb(self):
    batches = frappe.get_all(
        "Batch",
        filters={
            "reference_doctype": self.doctype,
            "reference_name": self.name,
        },
        fields=[
            "name",
            "custom_headcount_remaining",
            "custom_initial_headcount",
        ]
    )

    for b in batches:
        frappe.db.set_value(
            "Batch",
            b.name,
            {
                "custom_headcount_remaining": 0,
                "custom_initial_headcount": 0,
            }
        )

def update_batch_headcount(batch_no, qty_moved, headcount_change):
    batch = frappe.get_doc("Batch", batch_no)

    if not batch.custom_initial_headcount and qty_moved > 0:
        batch.custom_initial_headcount = headcount_change
        batch.custom_headcount_remaining = headcount_change
        batch.save(ignore_permissions=True)
        return

    if qty_moved < 0:
        batch.custom_headcount_remaining -= headcount_change
    else:
        batch.custom_headcount_remaining += headcount_change

    if batch.custom_headcount_remaining < 0:
        frappe.throw(
            f"Batch {batch.name} has insufficient livestock headcount"
        )

    batch.save(ignore_permissions=True)
    
def update_sabb_and_batches(sabb_name, weight_per_unit):
    sabb = frappe.get_doc("Serial and Batch Bundle", sabb_name)

    for entry in sabb.entries:
        entry_headcount = round(abs(entry.qty) / weight_per_unit)

        entry.custom_headcount = entry_headcount

        update_batch_headcount(
            entry.batch_no,
            entry.qty,
            entry_headcount
        )

    sabb.save(ignore_permissions=True)
        
def reverse_sabb(sabb_name):
    sabb = frappe.get_doc("Serial and Batch Bundle", sabb_name)

    touched_batches = set()

    for entry in sabb.entries:
        if entry.batch_no:
            touched_batches.add(entry.batch_no)

    for batch_no in touched_batches:
        frappe.db.set_value(
            "Batch",
            batch_no,
            {
                "custom_headcount_remaining": 0,
                "custom_initial_headcount": 0,
            }
        )

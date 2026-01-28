import frappe

def repost_livestock_headcount():
    sles = frappe.get_all(
        "Stock Ledger Entry",
        filters={"docstatus": 1, "custom_headcount": [">", 0]},
        fields=["name", "item_code", "custom_headcount", "actual_qty", "serial_and_batch_bundle", "voucher_no", "voucher_type", "voucher_detail_no"]
    )

    for sle in sles:
        item_doc = frappe.get_cached_doc("Item", sle.item_code)
        if not item_doc.custom_is_livestock:
            continue

        weight_per_unit = None
        if sle.voucher_type and sle.voucher_no and sle.voucher_detail_no:
            row = frappe.get_doc(sle.voucher_type, sle.voucher_no).get("items", {"name": sle.voucher_detail_no})
            if row:
                weight_per_unit = row[0].get("custom_weight_per_unit")

        if not weight_per_unit:
            weight_per_unit = item_doc.custom_weight_per_unit

        if not weight_per_unit:
            frappe.throw(f"Cannot determine weight per unit for item {item_doc.name}")

        if sle.serial_and_batch_bundle:
            repost_sabb_headcount(sle.serial_and_batch_bundle, weight_per_unit)

def repost_sabb_headcount(sabb_name, weight_per_unit):
    sabb = frappe.get_doc("Serial and Batch Bundle", sabb_name)

    for entry in sabb.entries:
        entry_headcount = round(abs(entry.qty) / weight_per_unit)
        entry.custom_headcount = entry_headcount

        if entry.batch_no:
            update_batch_headcount(entry.batch_no, entry.qty, entry_headcount)

    sabb.save(ignore_permissions=True)

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
        batch.custom_headcount_remaining = 0

    batch.save(ignore_permissions=True)

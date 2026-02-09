import frappe


def reset_livestock_batches():
    batches = frappe.get_all(
        "Batch",
        fields=["name"]
    )

    for b in batches:
        frappe.db.set_value(
            "Batch",
            b.name,
            {
                "custom_initial_weight": 0,
                "custom_weight_remaining": 0,
            }
        )

    frappe.db.commit()


def repost_livestock_weight():
    reset_livestock_batches()

    sles = frappe.get_all(
        "Stock Ledger Entry",
        filters={
            "docstatus": 1,
            "custom_weight_kg": ["!=", 0],
            "is_cancelled": 0,
        },
        fields=[
            "item_code",
            "actual_qty",
            "serial_and_batch_bundle",
            "voucher_no",
            "voucher_type",
            "voucher_detail_no",
            "posting_date",
            "posting_time",
            "creation",
        ],
        order_by="posting_date asc, posting_time asc, creation asc",
    )

    for sle in sles:
        item = frappe.get_cached_doc("Item", sle.item_code)
        if not item.custom_is_livestock:
            continue

        weight_per_unit = get_weight_per_unit(sle, item)

        if sle.serial_and_batch_bundle:
            repost_sabb_weight(
                sle.serial_and_batch_bundle,
                weight_per_unit,
                sle.actual_qty
            )


def get_weight_per_unit(sle, item):
    if sle.voucher_type and sle.voucher_no and sle.voucher_detail_no:
        doc = frappe.get_doc(sle.voucher_type, sle.voucher_no)
        row = doc.get("items", {"name": sle.voucher_detail_no})
        if row and row[0].custom_weight_per_unit:
            return row[0].custom_weight_per_unit

    if item.custom_weight_per_unit:
        return item.custom_weight_per_unit

    frappe.throw(
        f"Cannot determine weight per unit for livestock item {item.name}"
    )


def repost_sabb_weight(sabb_name, weight_per_unit, sle_actual_qty):
    sabb = frappe.get_doc("Serial and Batch Bundle", sabb_name)

    for entry in sabb.entries:
        # Weight should have the same sign as qty
        entry_weight = entry.qty * weight_per_unit  # ✅ Signed weight
        entry.custom_weight_kg = entry_weight

        if entry.batch_no:
            update_batch_weight(
                entry.batch_no,
                entry.qty,
                entry_weight
            )

    sabb.save(ignore_permissions=True)


def update_batch_weight(batch_no, qty_moved, moved_weight):
    batch = frappe.get_doc("Batch", batch_no)

    if qty_moved > 0:
        if not batch.custom_initial_weight:
            batch.custom_initial_weight = abs(moved_weight)
        
        batch.custom_weight_remaining += abs(moved_weight)
    else:
        batch.custom_weight_remaining -= abs(moved_weight)

    if batch.custom_weight_remaining < 0:
        batch.custom_weight_remaining = 0

    batch.save(ignore_permissions=True)
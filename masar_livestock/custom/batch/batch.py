import frappe
from frappe.utils import flt

##
##
def sum_weight(query, batch):
    data = frappe.db.sql(query, {"batch": batch}, as_dict=True)
    return sum(flt(d.weight) for d in data)


@frappe.whitelist()
def recalculate_livestock_weight(batch_name):
    in_weight = 0.0
    out_weight = 0.0

    in_weight += sum_weight("""
        SELECT
            (sbb_item.qty / pri.conversion_factor) AS weight
        FROM `tabPurchase Receipt Item` pri
        INNER JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
        INNER JOIN `tabSerial and Batch Entry` sbb_item
            ON sbb_item.parent = pri.serial_and_batch_bundle
        WHERE pr.docstatus = 1
          AND sbb_item.batch_no = %(batch)s
    """, batch_name)

    out_weight += sum_weight("""
        SELECT
            (sbb_item.qty / dni.conversion_factor) AS weight
        FROM `tabDelivery Note Item` dni
        INNER JOIN `tabDelivery Note` dn ON dn.name = dni.parent
        INNER JOIN `tabSerial and Batch Entry` sbb_item
            ON sbb_item.parent = dni.serial_and_batch_bundle
        WHERE dn.docstatus = 1
          AND sbb_item.batch_no = %(batch)s
    """, batch_name)

    out_weight += sum_weight("""
        SELECT
            (sbb_item.qty / sii.conversion_factor) AS weight
        FROM `tabSales Invoice Item` sii
        INNER JOIN `tabSales Invoice` si ON si.name = sii.parent
        INNER JOIN `tabSerial and Batch Entry` sbb_item
            ON sbb_item.parent = sii.serial_and_batch_bundle
        WHERE si.docstatus = 1
          AND si.update_stock = 1
          AND sbb_item.batch_no = %(batch)s
    """, batch_name)

    in_weight += sum_weight("""
        SELECT
            (sbb_item.qty / pii.conversion_factor) AS weight
        FROM `tabPurchase Invoice Item` pii
        INNER JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
        INNER JOIN `tabSerial and Batch Entry` sbb_item
            ON sbb_item.parent = pii.serial_and_batch_bundle
        WHERE pi.docstatus = 1
          AND pi.update_stock = 1
          AND sbb_item.batch_no = %(batch)s
    """, batch_name)

    se_data = frappe.db.sql("""
        SELECT
            se.stock_entry_type,
            (sbb_item.qty / sei.conversion_factor) AS weight
        FROM `tabStock Entry Detail` sei
        INNER JOIN `tabStock Entry` se ON se.name = sei.parent
        INNER JOIN `tabSerial and Batch Entry` sbb_item
            ON sbb_item.parent = sei.serial_and_batch_bundle
        WHERE se.docstatus = 1
          AND sbb_item.batch_no = %(batch)s
    """, {"batch": batch_name}, as_dict=True)

    for row in se_data:
        if row.stock_entry_type in ("Material Receipt", "Repack"):
            in_weight += flt(row.weight)
        else:
            out_weight += flt(row.weight)

    batch = frappe.get_doc("Batch", batch_name)
    batch.custom_in_weight_kg = in_weight
    batch.custom_out_weight_kg = out_weight
    batch.custom_current_weight_kg = in_weight - out_weight
    batch.save(ignore_permissions=True)

    return {
        "in_weight_kg": in_weight,
        "out_weight_kg": out_weight,
        "current_weight_kg": batch.custom_current_weight_kg
    }

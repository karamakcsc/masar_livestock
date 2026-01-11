import frappe
from frappe.utils import flt


def sum_weight(query, batch):
    data = frappe.db.sql(query, {"batch": batch}, as_dict=True)
    return sum(flt(d.weight) for d in data)


@frappe.whitelist()
def recalculate_livestock_weight(batch_name):
    in_weight = 0
    out_weight = 0

    # Purchase Receipt (IN)
    in_weight += sum_weight("""
        SELECT pri.qty * pri.conversion_factor AS weight
        FROM `tabPurchase Receipt Item` pri
        JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
        WHERE pr.docstatus = 1
          AND pri.batch_no = %(batch)s
    """, batch_name)

    # Delivery Note (OUT)
    out_weight += sum_weight("""
        SELECT dni.qty * dni.conversion_factor AS weight
        FROM `tabDelivery Note Item` dni
        JOIN `tabDelivery Note` dn ON dn.name = dni.parent
        WHERE dn.docstatus = 1
          AND dni.batch_no = %(batch)s
    """, batch_name)

    # Sales Invoice (OUT – update stock)
    out_weight += sum_weight("""
        SELECT sii.qty * sii.conversion_factor AS weight
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON si.name = sii.parent
        WHERE si.docstatus = 1
          AND si.update_stock = 1
          AND sii.batch_no = %(batch)s
    """, batch_name)

    # Purchase Invoice (IN – update stock)
    in_weight += sum_weight("""
        SELECT pii.qty * pii.conversion_factor AS weight
        FROM `tabPurchase Invoice Item` pii
        JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
        WHERE pi.docstatus = 1
          AND pi.update_stock = 1
          AND pii.batch_no = %(batch)s
    """, batch_name)

    # Stock Entry (IN & OUT)
    se_data = frappe.db.sql("""
        SELECT
            se.stock_entry_type,
            sei.qty * sei.conversion_factor AS weight
        FROM `tabStock Entry Detail` sei
        JOIN `tabStock Entry` se ON se.name = sei.parent
        WHERE se.docstatus = 1
          AND sei.batch_no = %(batch)s
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
        "in": in_weight,
        "out": out_weight,
        "current": batch.custom_current_weight_kg
    }

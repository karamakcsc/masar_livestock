import frappe
from frappe.utils import flt, cint, getdate


def validate_livestock_items(self):
    for row in self.items:
        item = frappe.get_doc("Item", row.item_code)

        if not item.custom_is_livestock:
            row.custom_weight_kg = None
            row.custom_weight_per_unit = None
            continue

        if not row.custom_weight_kg or row.custom_weight_kg < 0:
            frappe.throw(
                f"Weight Kg must be greater than zero "
                f"for livestock item {row.item_code} in row {row.idx}"
            )

        qty = flt(row.qty)

        if qty == 0:
            frappe.throw(f"Qty cannot be zero in row {row.idx}")

        weight_kg = abs(flt(row.custom_weight_kg))
        rate_kg = flt(getattr(row, "custom_rate_kg", 0))

        weight_per_unit = weight_kg / abs(qty)
        row.custom_weight_per_unit = weight_per_unit

        if rate_kg:
            base_rate = rate_kg * weight_per_unit

            if not self.is_return:
                row.rate = abs(base_rate)
            else:
                row.rate = abs(row.rate)

def set_weight_sle_sabb(self):
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
        if not row.custom_weight_kg:
            continue

        item = frappe.get_doc("Item", row.item_code)
        if not item.custom_is_livestock:
            continue

        for sle in sle_by_row.get(row.name, []):
            signed_weight = (
                abs(row.custom_weight_kg) 
                if sle.actual_qty > 0 
                else -abs(row.custom_weight_kg)
            )

            frappe.db.set_value(
                "Stock Ledger Entry",
                sle.name,
                "custom_weight_kg",
                signed_weight
            )

            if sle.serial_and_batch_bundle:
                update_sabb_and_batches_weight(
                    sle.serial_and_batch_bundle,
                    row.custom_weight_per_unit
                )


def reverse_weight_sle_sabb(self):
    sles = frappe.get_all(
        "Stock Ledger Entry",
        filters={
            "voucher_type": self.doctype,
            "voucher_no": self.name,
        },
        fields=[
            "name",
            "serial_and_batch_bundle",
            "actual_qty",
        ]
    )

    for sle in sles:
        if sle.serial_and_batch_bundle:
            reverse_sabb_and_batch_weight(
                sle.serial_and_batch_bundle,
                self.doctype,
                self.name
            )

    batches = frappe.get_all(
        "Batch",
        filters={
            "reference_doctype": self.doctype,
            "reference_name": self.name,
        },
        fields=["name"]
    )

    for b in batches:
        frappe.db.set_value(
            "Batch",
            b.name,
            {
                "custom_weight_remaining": 0,
                "custom_initial_weight": 0,
            }
        )


def reverse_sabb_and_batch_weight(sabb_name, voucher_type, voucher_no):
    sabb = frappe.get_doc("Serial and Batch Bundle", sabb_name)

    for entry in sabb.entries:
        if not entry.custom_weight_kg or not entry.batch_no:
            continue

        batch = frappe.get_doc("Batch", entry.batch_no)
        entry_weight = abs(entry.custom_weight_kg)

        is_creator = (
            batch.reference_doctype == voucher_type and 
            batch.reference_name == voucher_no
        )

        if entry.qty > 0:
            batch.custom_weight_remaining -= entry_weight
            if is_creator:
                batch.custom_initial_weight -= entry_weight
        else:
            batch.custom_weight_remaining += entry_weight

        if batch.custom_weight_remaining < 0:
            batch.custom_weight_remaining = 0
        
        if batch.custom_initial_weight < 0:
            batch.custom_initial_weight = 0

        batch.save(ignore_permissions=True)

def update_batch_weight(batch_no, qty_moved, weight_per_unit):
    batch = frappe.get_doc("Batch", batch_no)

    moved_weight = abs(qty_moved) * weight_per_unit

    if not batch.custom_initial_weight and qty_moved > 0:
        batch.custom_initial_weight = moved_weight
        batch.custom_weight_remaining = moved_weight
        batch.save(ignore_permissions=True)
        return

    if qty_moved < 0:
        batch.custom_weight_remaining -= moved_weight
    else:
        batch.custom_weight_remaining += moved_weight


    batch.save(ignore_permissions=True)

    
def update_sabb_and_batches_weight(sabb_name, weight_per_unit):
    sabb = frappe.get_doc("Serial and Batch Bundle", sabb_name)

    for entry in sabb.entries:
        entry_weight = abs(entry.qty) * weight_per_unit
        entry.custom_weight_kg = entry_weight

        update_batch_weight(
            entry.batch_no,
            entry.qty,
            weight_per_unit
        )

    sabb.save(ignore_permissions=True)


@frappe.whitelist()
def calculate_feed_cost(posting_date, item_code, feed_qty_per_day=None, feed_item=None):
    if not posting_date or not item_code:
        return
    
    feed_qty_per_day = flt(feed_qty_per_day)

    if feed_qty_per_day <= 0:
        feed_qty_per_day = frappe.db.get_single_value("Feed Settings", "default_feed_qty_per_day")
    if not feed_item:
        feed_item = frappe.db.get_single_value("Feed Settings", "default_feed_item")
    
        
    purchase_date = frappe.db.get_value("Batch", {"item": item_code}, "manufacturing_date")
    
    no_of_days = (getdate(posting_date) - getdate(purchase_date)).days + 1
    
    feed_cost_kg = frappe.db.get_value("Stock Ledger Entry", {"item_code": feed_item, "posting_date": ("<=", posting_date)}, "valuation_rate", order_by="posting_date desc")
    
    feed_cost_day = flt(feed_qty_per_day) * flt(feed_cost_kg)
    
    total_feed_cost = feed_cost_day * no_of_days
    
    return {
        "purchase_date": purchase_date,
        "no_of_days": no_of_days,
        "feed_item": feed_item,
        "feed_qty_per_day": feed_qty_per_day,
        "feed_cost_kg": feed_cost_kg,
        "feed_cost_day": feed_cost_day,
        "total_feed_cost": total_feed_cost
    }

def create_jv(self):

    exists = frappe.db.exists(
        "Journal Entry",
        {"custom_reference_doctype": self.doctype, "custom_reference_docname": self.name}
    )

    if exists:
        return

    dr_account = frappe.db.get_single_value("Feed Settings", "feed_consumption_debit")
    cr_account = frappe.db.get_single_value("Feed Settings", "feed_consumption_credit")
    dr_issue_account = frappe.db.get_single_value("Feed Settings", "feed_consumption_issue")

    feed_cost_amount = sum(
        flt(d.custom_total_feed_cost)
        for d in self.items
        if d.custom_is_livestock == 1
    )

    if not feed_cost_amount:
        return

    new_jv = frappe.new_doc("Journal Entry")
    new_jv.posting_date = self.posting_date
    new_jv.company = self.company
    new_jv.custom_reference_doctype = self.doctype
    new_jv.custom_reference_docname = self.name

    new_jv.append("accounts", {
        "account": dr_account,
        "debit_in_account_currency": feed_cost_amount,
        "debit": feed_cost_amount,
    })

    new_jv.append("accounts", {
        "account": cr_account if self.doctype != "Stock Entry" else dr_issue_account,
        "credit_in_account_currency": feed_cost_amount,
        "credit": feed_cost_amount,
    })

    new_jv.save(ignore_permissions=True)
    new_jv.submit()
import frappe
##

def validate(self, method):
    validate_items(self)

def validate_items(self):
    for item in self.items:
        item_doc = frappe.get_doc("Item", item.item_code)
        if item_doc.custom_is_livestock:
            if not item.custom_headcount:
                frappe.throw(f"Headcount is required for livestock item {item.item_code} in row {item.idx}.")
            if not item.custom_weight_kg:
                frappe.throw(f"Weight (Kg) is required for livestock item {item.item_code} in row {item.idx}.")
            if item.custom_weight_kg <= 0:
                frappe.throw(f"Weight (Kg) must be greater than zero for livestock item {item.item_code} in row {item.idx}.")
            if item.custom_headcount <= 0:
                frappe.throw(f"Headcount must be greater than zero for livestock item {item.item_code} in row {item.idx}.")
            conversion_factor = item.custom_headcount / item.custom_weight_kg
            # frappe.throw(f"Conversion Factor calculated as {conversion_factor} for item {item.item_code} in row {item.idx}.")
            item.conversion_factor = conversion_factor
            item.uom = "Kg"
            item.custom_weight_kg = item.qty
        else:
            item.custom_weight_kg = None
            item.custom_headcount = None
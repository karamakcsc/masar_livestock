import frappe
from masar_livestock.utilites import validate_livestock_items, set_weight_sle_sabb, reverse_weight_sle_sabb


def validate(doc, method):
    validate_livestock_items(doc)
def on_submit(self, method):
    if self.update_stock:
        set_weight_sle_sabb(self)
    pass
def on_cancel(self, method):
    if self.update_stock:
        reverse_weight_sle_sabb(self)
    pass
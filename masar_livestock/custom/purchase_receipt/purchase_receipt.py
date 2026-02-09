import frappe
from masar_livestock.utilites import validate_livestock_items, set_weight_sle_sabb, reverse_weight_sle_sabb


def validate(self, method):
    validate_livestock_items(self)
def on_submit(self, method):
    set_weight_sle_sabb(self)
def on_cancel(self, method):
    reverse_weight_sle_sabb(self)
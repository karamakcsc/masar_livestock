import frappe
from masar_livestock.utilites import validate_livestock_items, set_headcount_sle_sabb, reverse_headcount_sle_sabb


def validate(self, method):
    validate_livestock_items(self)
def on_submit(self, method):
    set_headcount_sle_sabb(self)
def on_cancel(self, method):
    reverse_headcount_sle_sabb(self)
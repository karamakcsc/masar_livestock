import frappe
from masar_livestock.utilites import validate_livestock_items


def validate(self, method):
    validate_livestock_items(self)
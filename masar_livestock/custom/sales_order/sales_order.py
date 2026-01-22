import frappe
from masar_livestock.utilites import validate_livestock_items


def validate(doc, method):
    validate_livestock_items(doc)

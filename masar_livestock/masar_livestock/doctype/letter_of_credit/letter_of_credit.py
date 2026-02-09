# Copyright (c) 2026, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LetterofCredit(Document):
	def validate(self):
		if self.purchase_order:
			exists = frappe.db.exists(self.doctype, {"purchase_order": self.purchase_order}, "name")
			if exists:
				frappe.throw(f"The Linked PO: {self.purchase_order} already has an existing Letter of Credit: {exists}")

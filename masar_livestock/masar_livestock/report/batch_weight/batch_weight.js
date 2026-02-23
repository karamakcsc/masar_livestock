// Copyright (c) 2026, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Batch Weight"] = {
	"filters": [
		{
			"fieldname": "item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "batch_no",
			"label": __("Batch No"),
			"fieldtype": "Link",
			"options": "Batch",
		}
	]
};

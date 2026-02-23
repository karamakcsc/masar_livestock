# Copyright (c) 2026, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_data(filters):
	conditions = " 1=1 "
	if filters.get("item_code"):
		conditions += f" AND sle.item_code = '{filters.get('item_code')}'"
	if filters.get("batch_no"):
		conditions += f" AND sle.batch_no = '{filters.get('batch_no')}'"

	data = frappe.db.sql(f"""
		SELECT
			sbb_item.batch_no AS batch,
			sle.item_code AS item,
			b.item_name AS item_name,
			b.custom_ship_name AS ship_name,
			b.manufacturing_date AS start_date,
			MIN(CASE WHEN sbb_item.qty > 0 THEN sbb_item.qty END) AS opening_qty,
			b.batch_qty AS remaining_qty,
			b.custom_initial_weight AS opening_weight,
			b.custom_weight_remaining AS remaining_weight
		FROM `tabStock Ledger Entry` sle
		INNER JOIN `tabSerial and Batch Bundle` sbb
			ON sbb.name = sle.serial_and_batch_bundle
		INNER JOIN `tabSerial and Batch Entry` sbb_item
			ON sbb_item.parent = sbb.name
		LEFT JOIN `tabBatch` b
			ON b.name = sbb_item.batch_no
		WHERE
			{conditions}
			AND sbb_item.batch_no IS NOT NULL
		GROUP BY sbb_item.batch_no, sle.item_code, b.manufacturing_date
	""", as_dict=True)

	return data

def get_columns():
	return [
		{"label": "Batch", "fieldname": "batch", "fieldtype": "Link", "options": "Batch", "width": 150},
		{"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
  		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
		{"label": "Ship Name", "fieldname": "ship_name", "fieldtype": "Data", "width": 150},
		{"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 120},
		{"label": "Opening Qty", "fieldname": "opening_qty", "fieldtype": "Float", "width": 120},
		{"label": "Remaining Qty", "fieldname": "remaining_qty", "fieldtype": "Float", "width": 120},
		{"label": "Opening Weight", "fieldname": "opening_weight", "fieldtype": "Float", "width": 130},
		{"label": "Remaining Weight", "fieldname": "remaining_weight", "fieldtype": "Float", "width": 130},
	]
frappe.ui.form.on('Stock Entry Detail', {
    custom_weight_kg: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.qty) {
            if (row.custom_weight_kg > 0 && row.qty > 0) {
                    let weight_per_unit = row.custom_weight_kg / row.qty;
                    frappe.model.set_value(cdt, cdn, "custom_weight_per_unit", weight_per_unit);
            }
        }
        frm.refresh_field("items");
    },
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.qty) {
            if (row.custom_weight_kg > 0 && row.qty > 0) {
                    let weight_per_unit = row.custom_weight_kg / row.qty;
                    frappe.model.set_value(cdt, cdn, "custom_weight_per_unit", weight_per_unit);
            }
        }
        frm.refresh_field("items");
    },
});

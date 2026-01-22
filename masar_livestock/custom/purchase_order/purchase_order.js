frappe.ui.form.on('Purchase Order Item', {
    custom_headcount: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.qty) {
            if (row.custom_headcount > 0 && row.qty > 0) {
                    let weight_per_unit = row.qty / row.custom_headcount;
                    frappe.model.set_value(cdt, cdn, "custom_weight_per_unit", weight_per_unit);
            }
        }
        frm.refresh_field("items");
    },
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.qty) {
            if (row.custom_headcount > 0 && row.qty > 0) {
                    let weight_per_unit = row.qty / row.custom_headcount;
                    frappe.model.set_value(cdt, cdn, "custom_weight_per_unit", weight_per_unit);
            }
        }
        frm.refresh_field("items");
    }
});

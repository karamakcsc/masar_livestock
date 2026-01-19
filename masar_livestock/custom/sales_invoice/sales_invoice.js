frappe.ui.form.on('Sales Invoice Item', {
    item_code: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.item_code) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Item",
                    name: row.item_code
                },
                callback: function (data) {
                    let item = data.message;
                    if (item && item.custom_is_livestock) {
                        setTimeout(() => {
                            frappe.model.set_value(cdt, cdn, "uom", "Kg");
                            frappe.model.set_df_property(cdt, cdn, "uom", "read_only", 1);
                            frappe.model.set_df_property(cdt, cdn, "custom_weight_kg", "read_only", 0);
                            frappe.model.set_df_property(cdt, cdn, "custom_headcount", "read_only", 0);
                            console.log("Item code changed, UOM set to Kg and made read-only.");
                        }, 600);
                    } else {
                        setTimeout(() => {
                            frappe.model.set_value(cdt, cdn, "custom_headcount", null);
                            frappe.model.set_value(cdt, cdn, "custom_weight_kg", null);
                            frappe.model.set_df_property(cdt, cdn, "uom", "read_only", 0);
                            frappe.model.set_df_property(cdt, cdn, "custom_weight_kg", "read_only", 1);
                            frappe.model.set_df_property(cdt, cdn, "custom_headcount", "read_only", 1);
                            console.log("Item code changed, UOM made editable.");
                        }, 600);
                    }
                }
            });
        }
        frm.refresh_field("items");
    },
    custom_headcount: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.custom_weight_kg) {
            if (row.custom_headcount > 0 && row.custom_weight_kg > 0) {
                setTimeout(() => {
                    let conversion_factor = row.custom_headcount / row.custom_weight_kg;
                    frappe.model.set_value(cdt, cdn, "qty", row.custom_weight_kg);
                    frappe.model.set_value(cdt, cdn, "stock_qty", row.custom_headcount);
                    frappe.model.set_value(cdt, cdn, "conversion_factor", conversion_factor);
                }, 600);
            }
        }
        frm.refresh_field("items");
    },
    custom_weight_kg: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.custom_weight_kg) {
            if (row.custom_headcount > 0 && row.custom_weight_kg > 0) {
                setTimeout(() => {
                    let conversion_factor = row.custom_headcount / row.custom_weight_kg;
                    frappe.model.set_value(cdt, cdn, "qty", row.custom_weight_kg);
                    frappe.model.set_value(cdt, cdn, "stock_qty", row.custom_headcount);
                    frappe.model.set_value(cdt, cdn, "conversion_factor", conversion_factor);
                }, 600);
            }
        }
        frm.refresh_field("items");
    }
});

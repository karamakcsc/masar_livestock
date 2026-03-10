frappe.ui.form.on('Sales Invoice Item', {
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
    custom_rate_kg: function(frm,cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.custom_weight_per_unit && row.custom_rate_kg) {
            if (row.custom_rate_kg > 0 && row.custom_weight_per_unit > 0) {
                    let rate_per_unit = row.custom_weight_per_unit * row.custom_rate_kg;
                    frappe.model.set_value(cdt, cdn, "rate", rate_per_unit);
            }
        }
        frm.refresh_field("items");
    },
    item_code: function(frm, cdt, cdn) {
        if (frm.doc.update_stock) {
            calculate_feed_cost(frm, cdt, cdn);
        }
    },
    custom_feed_qty_per_day: function(frm, cdt, cdn) {
        if (frm.doc.update_stock) {
            calculate_feed_cost(frm, cdt, cdn);
        }
    }
});

frappe.ui.form.on("Sales Invoice", {
    validate: function(frm) {
        if (frm.doc.update_stock) {
            frm.doc.items.forEach(function(item) {
                if (item.custom_is_livestock) {
                    calculate_feed_cost(frm, item.doctype, item.name);
                }
            });
        }
    }
});


function calculate_feed_cost(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.item_code && row.custom_is_livestock) {
        let posting_date = frm.doc.posting_date;
        let item_code = row.item_code;
        let feed_qty_per_day = row.custom_feed_qty_per_day;
        let feed_item = row.custom_feed_item;
        
        frappe.call({
            method: "masar_livestock.utilites.calculate_feed_cost",
            args: {
                posting_date: posting_date,
                item_code: item_code,
                feed_qty_per_day: feed_qty_per_day,
                feed_item: feed_item
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, "custom_purchase_date", r.message.purchase_date);
                    frappe.model.set_value(cdt, cdn, "custom_no_of_days", r.message.no_of_days);
                    frappe.model.set_value(cdt, cdn, "custom_feed_item", r.message.feed_item);
                    frappe.model.set_value(cdt, cdn, "custom_feed_qty_per_day", r.message.feed_qty_per_day);
                    frappe.model.set_value(cdt, cdn, "custom_feed_cost_per_kg", r.message.feed_cost_kg);
                    frappe.model.set_value(cdt, cdn, "custom_feed_cost_per_day", r.message.feed_cost_day);
                    frappe.model.set_value(cdt, cdn, "custom_total_feed_cost", r.message.total_feed_cost);
                    frm.refresh_field("items");
                    console.log(r.message);
                }
            }
        });
    }
}
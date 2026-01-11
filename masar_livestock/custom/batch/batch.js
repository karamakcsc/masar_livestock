frappe.ui.form.on("Batch", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(
                __("Recalculate Livestock Weight"),
                () => {
                    frappe.call({
                        method: "masar_livestock.custom.batch.batch.recalculate_livestock_weight",
                        args: {
                            batch_name: frm.doc.name
                        },
                        freeze: true,
                        callback(r) {
                            if (r.message) {
                                frm.reload_doc();
                                frappe.msgprint({
                                    title: __("Weight Updated"),
                                    message: __(
                                        `IN: ${r.message.in} Kg<br>
                                         OUT: ${r.message.out} Kg<br>
                                         CURRENT: ${r.message.current} Kg`
                                    ),
                                    indicator: "green"
                                });
                            }
                        }
                    });
                }
            );
        }
    }
});

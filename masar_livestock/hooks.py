app_name = "masar_livestock"
app_title = "Masar Livestock"
app_publisher = "KCSC"
app_description = "livestock"
app_email = "info@kcsc.com.jo"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "masar_livestock",
# 		"logo": "/assets/masar_livestock/logo.png",
# 		"title": "Masar Livestock",
# 		"route": "/masar_livestock",
# 		"has_permission": "masar_livestock.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/masar_livestock/css/masar_livestock.css"
# app_include_js = "/assets/masar_livestock/js/masar_livestock.js"

# include js, css files in header of web template
# web_include_css = "/assets/masar_livestock/css/masar_livestock.css"
# web_include_js = "/assets/masar_livestock/js/masar_livestock.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "masar_livestock/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Purchase Receipt" : "custom/purchase_receipt/purchase_receipt.js",
    "Purchase Order" : "custom/purchase_order/purchase_order.js",
    "Purchase Invoice" : "custom/purchase_invoice/purchase_invoice.js",
    "Sales Order" : "custom/sales_order/sales_order.js",
    "Delivery Note" : "custom/delivery_note/delivery_note.js",
    "Stock Entry" : "custom/stock_entry/stock_entry.js",
    "Sales Invoice" : "custom/sales_invoice/sales_invoice.js",
    "Batch": "custom/batch/batch.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "masar_livestock/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "masar_livestock.utils.jinja_methods",
# 	"filters": "masar_livestock.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "masar_livestock.install.before_install"
# after_install = "masar_livestock.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "masar_livestock.uninstall.before_uninstall"
# after_uninstall = "masar_livestock.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "masar_livestock.utils.before_app_install"
# after_app_install = "masar_livestock.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "masar_livestock.utils.before_app_uninstall"
# after_app_uninstall = "masar_livestock.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "masar_livestock.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Purchase Receipt": {
		"validate": "masar_livestock.custom.purchase_receipt.purchase_receipt.validate",
        "on_submit": "masar_livestock.custom.purchase_receipt.purchase_receipt.on_submit",
        "on_cancel": "masar_livestock.custom.purchase_receipt.purchase_receipt.on_cancel",
	},
    "Purchase Order": {
        "validate": "masar_livestock.custom.purchase_order.purchase_order.validate",
    },
    "Purchase Invoice": {
        "validate": "masar_livestock.custom.purchase_invoice.purchase_invoice.validate",
        "on_submit": "masar_livestock.custom.stock_entry.stock_entry.on_submit",
        "on_cancel": "masar_livestock.custom.stock_entry.stock_entry.on_cancel",
    },
    "Sales Order": {
        "validate": "masar_livestock.custom.sales_order.sales_order.validate",
    },
    "Delivery Note": {
        "validate": "masar_livestock.custom.delivery_note.delivery_note.validate",
        "on_submit": "masar_livestock.custom.stock_entry.stock_entry.on_submit",
        "on_cancel": "masar_livestock.custom.stock_entry.stock_entry.on_cancel",
    },
    "Stock Entry": {
        "validate": "masar_livestock.custom.stock_entry.stock_entry.validate",
        "on_submit": "masar_livestock.custom.stock_entry.stock_entry.on_submit",
        "on_cancel": "masar_livestock.custom.stock_entry.stock_entry.on_cancel",
    },
    "Sales Invoice": {
        "validate": "masar_livestock.custom.sales_invoice.sales_invoice.validate",
        "on_submit": "masar_livestock.custom.stock_entry.stock_entry.on_submit",
        "on_cancel": "masar_livestock.custom.stock_entry.stock_entry.on_cancel",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"masar_livestock.tasks.all"
# 	],
	"daily": [
		"masar_livestock.jobs.repost_headcount.repost_livestock_headcount"
	],
# 	"hourly": [
# 		"masar_livestock.tasks.hourly"
# 	],
# 	"weekly": [
# 		"masar_livestock.tasks.weekly"
# 	],
# 	"monthly": [
# 		"masar_livestock.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "masar_livestock.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "masar_livestock.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "masar_livestock.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["masar_livestock.utils.before_request"]
# after_request = ["masar_livestock.utils.after_request"]

# Job Events
# ----------
# before_job = ["masar_livestock.utils.before_job"]
# after_job = ["masar_livestock.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"masar_livestock.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
                "Item-custom_is_livestock",
                "Purchase Receipt Item-custom_headcount",
                "Purchase Invoice Item-custom_headcount",
                "Delivery Note Item-custom_headcount",
                "Sales Invoice Item-custom_headcount",
                "Stock Entry Detail-custom_headcount",
                "Purchase Order Item-custom_headcount",
                "Sales Order Item-custom_headcount",
                "Batch-custom_current_weight_kg",
                "Batch-custom_in_weight_kg",
                "Batch-custom_out_weight_kg",
                "Purchase Receipt Item-custom_is_livestock",
                "Purchase Order Item-custom_is_livestock",
                "Purchase Invoice Item-custom_is_livestock",
                "Sales Order Item-custom_is_livestock",
                "Delivery Note Item-custom_is_livestock",
                "Stock Entry Detail-custom_is_livestock",
                "Sales Invoice Item-custom_is_livestock",
                "Delivery Note Item-custom_weight_per_unit",
                "Sales Invoice Item-custom_weight_per_unit",
                "Sales Order Item-custom_weight_per_unit",
                "Purchase Invoice Item-custom_weight_per_unit",
                "Purchase Receipt Item-custom_weight_per_unit",
                "Purchase Order Item-custom_weight_per_unit",
                "Stock Entry Detail-custom_weight_per_unit"
            ]
        ]
    ]},
    {"dt": "Property Setter", "filters": [
        [
            "name", "in", [
                "Purchase Receipt Item-rate-columns",
                "Purchase Order Item-rate-columns",
                "Purchase Order Item-amount-columns",
                "Purchase Invoice Item-qty-columns",
                "Purchase Invoice Item-rate-columns",
                "Sales Order Item-delivery_date-columns",
                "Sales Order Item-rate-columns",
                "Delivery Note Item-uom-columns",
                "Delivery Note Item-qty-columns",
                "Stock Entry Detail-qty-columns",
                "Stock Entry Detail-basic_rate-columns",
                "Sales Invoice Item-qty-columns",
                "Sales Invoice Item-rate-columns",
                "Purchase Order Item-uom-read_only_depends_on",
                "Purchase Receipt Item-uom-read_only_depends_on",
                "Purchase Invoice Item-uom-read_only_depends_on",
                "Sales Order Item-uom-read_only_depends_on",
                "Sales Invoice Item-uom-read_only_depends_on",
                "Delivery Note Item-uom-read_only_depends_on",
                "Stock Entry Detail-uom-read_only_depends_on"
            ]
        ]
    ]},
]
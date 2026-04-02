frappe.query_reports["Leave Ledger Summary Test"] = {
    "filters": [
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "fieldname": "fiscal_year",
            "label": __("Fiscal Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "default": "2026",
            "reqd": 1,
        },
        {
            "fieldname": "target_date",
            "label": __("Target Date"),
            "fieldtype": "Date",
            "reqd": 1,
        }
    ]
};

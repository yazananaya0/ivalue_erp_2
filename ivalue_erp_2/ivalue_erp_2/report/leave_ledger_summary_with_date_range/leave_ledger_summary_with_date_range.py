import frappe
from frappe.utils import getdate


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
			"options": "Employee",
            "width": 200,
        },
        {
            "label": "Leave Type",
            "fieldname": "leave_type",
            "fieldtype": "Link",
            "options": "Leave Type",
            "width": 150,
        },
        {
            "label": "Leave Balance",
            "fieldname": "leave_balance",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Start Date",
            "fieldname": "start_date",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Year",
            "fieldname": "year",
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "width": 100
        },
    ]


def get_data(filters):
    fy = None
    if filters.get("fiscal_year"):
        fy = frappe.get_doc("Fiscal Year", filters.get("fiscal_year"))
        year = fy.name

    lle_filters = {"docstatus": 1}

    if filters.get("employee"):
        lle_filters["employee"] = filters.get("employee")

    if fy:
        if filters.get("target_date"):
            lle_filters["from_date"] = [
                "between",
                [fy.year_start_date, getdate(filters.get("target_date"))],
            ]
        else:
            lle_filters["from_date"] = [
                "between",
                [fy.year_start_date, fy.year_end_date],
            ]

    lle_list = frappe.get_all(
            
        "Leave Ledger Entry",
        fields=[
            "employee",
            "employee_name",
            "leave_type",
            "leaves",
            "from_date" 
        ],
        filters=lle_filters,
    )

    result = {}

    for lle in lle_list:
        if not lle.from_date:
            continue

        key = (lle.employee, lle.leave_type, year)

        if key not in result:
            result[key] = {
                "employee": f"{lle.employee}: {lle.employee_name}",
                "leave_type": lle.leave_type,
                "leave_balance": 0,
                "start_date": year+"-01-01",
                "year": year,
            }

        result[key]["leave_balance"] += lle.leaves

    data = list(result.values())

    data.sort(key=lambda x: (x["employee"], x["leave_type"]))

    return data
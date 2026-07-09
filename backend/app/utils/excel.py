from openpyxl import Workbook


def create_maintenance_excel(records):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Maintenance Report"

    headers = [
        "Flat Number",
        "Owner Name",
        "Email",
        "Phone",
        "Month",
        "Year",
        "Amount",
        "Status",
        "Due Date",
    ]

    sheet.append(headers)

    for record in records:
        sheet.append([
            record["flat_number"],
            record["owner_name"],
            record["email"],
            record["phone"],
            record["month"],
            record["year"],
            record["amount"],
            record["status"],
            str(record["due_date"]),
        ])

    file_name = "maintenance_report.xlsx"
    workbook.save(file_name)

    return file_name
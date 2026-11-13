"""Append unique employee rows from New_Records_10.xlsx to Master_Records_100.xlsx.

Intended to run via the local Jenkins Windows job or from Python directly.
Run it as many times as you want; existing Employee IDs are skipped.
"""

from copy import copy
from pathlib import Path
import sys

from openpyxl import load_workbook

BASE_DIR = Path(__file__).resolve().parent
MASTER_FILE = BASE_DIR / "Master_Records_100.xlsx"
INCOMING_FILE = BASE_DIR / "New_Records_10.xlsx"
SHEET = "Records"
EXPECTED_HEADERS = (
    "Employee ID",
    "Employee Name",
    "Department",
    "City",
    "Monthly Salary (USD)",
)


def data_row_count(ws):
    """Count genuine records rather than assuming Excel's max_row is exact."""
    return sum(
        1 for (employee_id, *_) in ws.iter_rows(min_row=2, values_only=True)
        if employee_id is not None and str(employee_id).strip()
    )


def check_headers(ws, file_name):
    headers = tuple(ws.cell(1, i).value for i in range(1, len(EXPECTED_HEADERS) + 1))
    if headers != EXPECTED_HEADERS:
        raise ValueError(
            f"Wrong column headers in {file_name}.\n"
            f"  Expected: {EXPECTED_HEADERS}\n"
            f"  Found:    {headers}"
        )


def append_one_row(ws, values):
    """Append data and copy formatting from the previous employee row."""
    previous_row = ws.max_row
    next_row = previous_row + 1
    for index, value in enumerate(values, start=1):
        target = ws.cell(next_row, index, value)
        template = ws.cell(previous_row, index)
        if template.has_style:
            target.font = copy(template.font)
            target.fill = copy(template.fill)
            target.border = copy(template.border)
            target.alignment = copy(template.alignment)
            target.number_format = template.number_format
            target.protection = copy(template.protection)
    if ws.row_dimensions[previous_row].height:
        ws.row_dimensions[next_row].height = ws.row_dimensions[previous_row].height


def main():
    for path in (MASTER_FILE, INCOMING_FILE):
        if not path.is_file():
            raise FileNotFoundError(f"Missing file: {path}")

    master = load_workbook(MASTER_FILE)
    incoming = load_workbook(INCOMING_FILE, read_only=True, data_only=True)
    try:
        if SHEET not in master.sheetnames or SHEET not in incoming.sheetnames:
            raise ValueError(f"Both workbooks must have a sheet named '{SHEET}'.")

        main_sheet = master[SHEET]
        new_sheet = incoming[SHEET]
        check_headers(main_sheet, MASTER_FILE.name)
        check_headers(new_sheet, INCOMING_FILE.name)

        before = data_row_count(main_sheet)
        existing_ids = {
            str(row[0]).strip()
            for row in main_sheet.iter_rows(min_row=2, max_col=len(EXPECTED_HEADERS), values_only=True)
            if row[0] is not None and str(row[0]).strip()
        }

        to_add = []
        duplicates = 0
        for row_number, row in enumerate(
            new_sheet.iter_rows(min_row=2, max_col=len(EXPECTED_HEADERS), values_only=True),
            start=2,
        ):
            record = tuple(row)
            if all(value is None or str(value).strip() == "" for value in record):
                continue
            employee_id = record[0]
            if employee_id is None or str(employee_id).strip() == "":
                raise ValueError(f"Missing Employee ID at incoming row {row_number}")
            key = str(employee_id).strip()
            if key in existing_ids:
                duplicates += 1
                continue
            existing_ids.add(key)
            to_add.append(record)

        print("JENKINS EXCEL UPDATE")
        print("-" * 42)
        print(f"Master file:   {MASTER_FILE}")
        print(f"Incoming file: {INCOMING_FILE}")
        print(f"Before build:  {before} records")
        print(f"New records:   {len(to_add)}")
        print(f"Duplicates:    {duplicates} skipped")

        for record in to_add:
            append_one_row(main_sheet, record)

        if to_add:
            try:
                master.save(MASTER_FILE)
            except PermissionError as error:
                raise PermissionError(
                    f"Cannot save {MASTER_FILE}. Close this Excel file if it is open, "
                    "and check the Jenkins Windows service account's file permissions."
                ) from error

        print(f"After build:   {before + len(to_add)} records")
        print("SUCCESS - master Excel is up to date.")
    finally:
        incoming.close()
        master.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        sys.exit(1)

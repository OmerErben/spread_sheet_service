import copy
import uuid

# In this file I define the main spreadsheet service


def finalize_value(sheet, col, row):
    # I assume that if I have a lookup function for a cell that wasn't defined yet, the default value is None
    if row not in sheet.cells[col]:
        return None
    elif type(sheet.cells[col][row]) != tuple:
        return sheet.cells[col][row]
    return finalize_value(sheet, sheet.cells[col][row][0], sheet.cells[col][row][1])


class SpreadSheetService:
    def __init__(self):
        self.sheets = {}

    def create_new_sheet(self, sheet):
        try:
            if not hasattr(sheet, "columns") or not hasattr(sheet, "cells") or not hasattr(sheet, "lookup_pairs"):
                raise ValueError("Invalid input. Object is not a legal spreadsheet")
            sheet_id = str(uuid.uuid4())
            self.sheets[sheet_id] = sheet
            print("New sheet created successfully")
            return sheet_id
        except Exception as ex:
            print(str(ex))
            return ex.args[0]

    def set_sheet_cell(self, sheet_id, col, row, value):
        try:
            sheet = self.sheets.get(sheet_id, None)
            if not sheet:
                raise ValueError("Invalid input. There's no sheet with this id")
            # Check if it's a lookup
            if type(value) == str and len(value) >= 10 and value[:7] == "lookup(" and value[-1] == ")":
                sheet.set_cell_lookup(col, row, value)
            else:
                sheet.set_cell(col, row, value)
        except Exception as ex:
            print(str(ex))

    def get_sheet_by_id(self, sheet_id):
        try:
            sheet = self.sheets.get(sheet_id, None)
            if not sheet:
                raise ValueError("Invalid input. There's no sheet with this id")
            sheet_cells = copy.deepcopy(sheet.cells)
            for pair in sheet.lookup_pairs.keys():
                sheet_cells[pair[0]][pair[1]] = finalize_value(sheet, pair[0], pair[1])
            return sheet_cells
        except Exception as ex:
            print(str(ex))
            return ex.args[0]

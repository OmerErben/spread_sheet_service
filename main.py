from spread_sheet import SpreadSheet, Column
from spread_sheet_service import SpreadSheetService

# Example run case
service = SpreadSheetService()
spread_sheet = SpreadSheet([Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                           Column("E", bool), Column("F", bool)])
sheet_id = service.create_new_sheet(spread_sheet)
service.set_sheet_cell(sheet_id, "A", 10, "hello")
service.set_sheet_cell(sheet_id, "B", 11, True)
service.set_sheet_cell(sheet_id, "B", 10, True)
# Create a loop
service.set_sheet_cell(sheet_id, "E", 11, "lookup(F,11)")
service.set_sheet_cell(sheet_id, "B", 11, "lookup(E,11)")
service.set_sheet_cell(sheet_id, "F", 11, "lookup(B,11)")
# Create a lookup to an uninitialized column
service.set_sheet_cell(sheet_id, "F", 10, "lookup(K,12)")
# Create a self loop
service.set_sheet_cell(sheet_id, "F", 14, "lookup(F,14)")
# Create a proper lookup
service.set_sheet_cell(sheet_id, "F", 13, "lookup(B,10)")
service.set_sheet_cell(sheet_id, "F", 13, False)

sheet = service.get_sheet_by_id(sheet_id)
print(sheet)


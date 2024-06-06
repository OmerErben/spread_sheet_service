# spread_sheet_service

### Methods

* create_new_sheet: Accepts as input a valid sheet object and initializes a new sheet in the service
* set_sheet_cell: Accepts as input a sheet id, column name, row index and value. This method sets the value of the cell to the value input
* get_sheet_by_id: Accepts as input a sheet id. This method will present the values of the cells in the sheet.

### Usage

Below is an example for how to use the service:
```python
from spread_sheet import SpreadSheet, Column
from spread_sheet_service import SpreadSheetService
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
```

You can run main.py to see the results

### Tests
All the tests are in the tests.py file. You can run them by running the Tester class.
#### Success Test Cases
* Create a new sheet
* Create an empty new sheet
* Create multiple sheets
* Set a lookup (single, multiple-hop, multiple lookups, changing values & uninitialized cell target)
* Overwrite a cell value

#### Failure Test Cases
* Use an invalid sheet id
* Set a cell to a wrong data type (also with lookup)
* Set a cell in a non-existing column
* Set a cell to a lookup to a non-existing column
* Set a self-cycle lookup
* Set a cycle lookup
* Set to a wrong lookup format


### Assumptions
* I assume that I need to present the values of the sheet when get_sheet_by_id is called
* I assume that it's impossible to add new columns after creating the sheet
* I assume that the default value for a lookup cell is None, until the target cell is initialized
* I decided to ignore lowercase and uppercase column names. All the columns are uppercase
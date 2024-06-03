# In this file I define all the classes for this assignment


class Column:
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type


class SpreadSheet:
    def __init__(self, spread_sheet_obj):
        self.columns = {col.name: col for col in spread_sheet_obj}
        self.cells = {col.name: {} for col in spread_sheet_obj}
        self.lookup_pairs = {}

    def set_cell(self, column_name, row_idx, value):
        try:
            dest_col = self.columns.get(column_name, None)
            # Check that the column exists
            if not dest_col:
                raise ValueError("Column not in sheet")
            # Check same data type
            if not dest_col.column_type == type(value):
                raise ValueError("Wrong data type for column of type {}".format(dest_col.column_type))
            self.cells[column_name][row_idx] = value
            # Delete the lookup pair if there is one
            if (column_name, row_idx) in self.lookup_pairs:
                del self.lookup_pairs[(column_name, row_idx)]
            print("Cell value was set successfully to {}".format(value))
        except Exception as ex:
            print(ex)

    def set_cell_lookup(self, column_name, row_idx, lookup):
        try:
            dest_col = self.columns.get(column_name, None)
            # Check that the column exists
            if not dest_col:
                raise ValueError("Column not in sheet")
            # Get the col and row from the lookup
            target = lookup.split("(")[1][:-1].split(",")
            lookup_col = self.columns.get(target[0], None)
            # Check that the lookup column exists
            if not lookup_col:
                raise ValueError("Lookup column not in sheet")
            # Check same data type
            if dest_col.column_type != lookup_col.column_type:
                raise ValueError("The columns don't have the same data type")
            target[1] = int(target[1])
            # Check for cycle
            if (column_name == target[0] and row_idx == target[1]) \
                    or self.check_cycle(target[0], (target[1]), {(column_name, row_idx)}):
                raise ValueError("This lookup creates a loop")
            self.cells[column_name][row_idx] = (target[0], target[1])
            # Keep the pair for the get sheet function
            self.lookup_pairs[(column_name, row_idx)] = (target[0], target[1])
            print("Cell value was set successfully to {}".format(lookup))
        except Exception as ex:
            print(ex)

    def check_cycle(self, col, row, visited_set):
        try:
            if row not in self.cells[col]:
                return False  # That value wasn't initialized yet, so there is no cycle
            value = self.cells[col][row]
            if type(value) != tuple:
                return False  # That value wasn't a lookup, so there is no cycle
            new_col, new_row = value[0], value[1]
            if (new_col, new_row) in visited_set:
                return True
            visited_set.add((col, row))
            return self.check_cycle(new_col, new_row, visited_set)
        except Exception as ex:
            print(ex)
            return ex






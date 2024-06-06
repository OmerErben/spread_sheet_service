from unittest import TestCase
from spread_sheet import SpreadSheet, Column
from spread_sheet_service import SpreadSheetService


def prep_test(service, cols):
    spread_sheet = SpreadSheet(cols)
    return service.create_new_sheet(spread_sheet)


class Tester(TestCase):

    def test_create(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float)])
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet), 4)
        for i in ["A", "B", "C", "D"]:
            self.assertEqual(len(sheet[i]), 0)

    def test_create_empty(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [])
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet), 0)

    def test_create_multiple(self):
        service = SpreadSheetService()
        sheet_id_1 = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float)])
        sheet_id_2 = prep_test(service, [Column("E", str), Column("F", bool), Column("G", str), Column("H", float),
                                         Column("I", float)])
        sheet_1 = service.get_sheet_by_id(sheet_id_1)
        sheet_2 = service.get_sheet_by_id(sheet_id_2)
        self.assertEqual(len(sheet_1), 4)
        self.assertEqual(len(sheet_2), 5)

    def test_lookup(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        service.set_sheet_cell(sheet_id, "A", 10, "hello")
        service.set_sheet_cell(sheet_id, "B", 10, True)
        service.set_sheet_cell(sheet_id, "F", 13, "lookup(B,10)")
        sheet = service.get_sheet_by_id(sheet_id)
        # Test simple lookup
        self.assertEqual(sheet["F"][13], True)
        # 2 hop-lookup
        service.set_sheet_cell(sheet_id, "E", 13, "lookup(F,13)")
        # 2nd lookup
        service.set_sheet_cell(sheet_id, "B", 11, "lookup(B,10)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(sheet["E"][13], True)
        self.assertEqual(sheet["B"][11], True)
        # Change the target value
        service.set_sheet_cell(sheet_id, "B", 10, False)
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(sheet["E"][13], False)
        # Create a lookup to an uninitialized cell, value would be None
        service.set_sheet_cell(sheet_id, "A", 10, "lookup(C, 1)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(sheet["A"][10], None)

    def test_overwrite(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        service.set_sheet_cell(sheet_id, "A", 10, "hello")
        service.set_sheet_cell(sheet_id, "A", 10, "test")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(sheet["A"][10], "test")

    def test_wrong_sheet_id(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        self.assertEqual(service.get_sheet_by_id(sheet_id + "test"),
                         "Invalid input. There's no sheet with this id")

    def test_wrong_col_type(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        service.set_sheet_cell(sheet_id, "A", 2, 2)
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet["A"]), 0)
        # Test wrong column type with lookup
        service.set_sheet_cell(sheet_id, "A", 2, "lookup(B, 2)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet["A"]), 0)

    def test_no_col_set(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        # K is not a column in the sheet, thus the set won't succeed.
        service.set_sheet_cell(sheet_id, "K", 1, 1)
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual("K" in sheet, False)

    def test_no_col_lookup(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        # K is not a column in the sheet, thus the set won't succeed.
        service.set_sheet_cell(sheet_id, "A", 1, "lookup(K, 2)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet["A"]), 0)

    def test_self_cycle_lookup(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        service.set_sheet_cell(sheet_id, "A", 10, "lookup(A, 10)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet["A"]), 0)

    def test_cycle_lookup(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        # 2 cell cycle
        service.set_sheet_cell(sheet_id, "A", 10, "lookup(A, 11)")
        # The following line creates a loop and thus won't be added to the sheet
        service.set_sheet_cell(sheet_id, "A", 11, "lookup(A, 10)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet["A"]), 1)
        # 3 cell cycle
        service.set_sheet_cell(sheet_id, "A", 11, "lookup(A, 12)")
        # The following line creates a loop and thus won't be added to the sheet
        service.set_sheet_cell(sheet_id, "A", 12, "lookup(A, 10)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(len(sheet["A"]), 2)

    def test_lookup_format(self):
        service = SpreadSheetService()
        sheet_id = prep_test(service, [Column("A", str), Column("B", bool), Column("C", str), Column("D", float),
                                       Column("E", bool), Column("F", bool)])
        service.set_sheet_cell(sheet_id, "A", 10, "lookup(A, 11")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(sheet["A"][10], "lookup(A, 11")
        service.set_sheet_cell(sheet_id, "A", 10, "lookupA, 11)")
        sheet = service.get_sheet_by_id(sheet_id)
        self.assertEqual(sheet["A"][10], "lookupA, 11)")

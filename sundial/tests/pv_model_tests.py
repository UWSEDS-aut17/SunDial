import os
os.chdir('../')
import unittest
import numpy as np
from sundial import pv_model



class UtilsTest(unittest.TestCase):

    def test_smoke(self):
        year = 2016
        month = 12
        day = 12
        pv_model.get_data_split(year, month, day)

    def test_smoke2(self):
        saved_model = 'finalized_model.pkl'
        y_pred = self.pv_model.save_model(saved_model)
        self.assertIsNotNone(y_pred)

    def test_smoke3(self):
        saved_model = 'finalized_model.pkl'
        year = 2016
        month = 12
        day = 15
        y_pred = self.pv_model.load_model(saved_model, year, month, day)
        self.assertTrue(len(y_pred), 24)

    def test_smoke4(self):
        saved_model = 'finalized_model.pkl'
        year = 2016
        month = 12
        day = 17
        pv_model.pv_output_cph(saved_model, year, month, day)

    def test_output_len(self):
        pv_output = self.pv_model.pv_output_cph(saved_model, year, month, day)
        self.assertTrue(len(pv_output), 24)

    def OutputTest(self):
        with self.assertRaises(Exception):
            try:
                pv_model.pv_output_cph()
            except Exception:
                pass
            else:
                raise Exception

    def Output_initialization_Test(self):
        with self.assertRaises(Exception):
            pv_model.pv_output_cph()


if __name__ == '__main__':
    unittest.main()

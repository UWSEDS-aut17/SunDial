import os
os.chdir('../')
import unittest
from sundial.price_model import price_model

class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.emp_train = price_model.EnergyPriceModel(train=True)
        self.emp_test = price_model.EnergyPriceModel()

    def test_smoke(self):
        price_out = self.emp_test.test_model("2016-12-12", 'SVM_rbf')
        self.assertIsNotNone(price_out)

    def test_smoke_training(self):
        try:
            self.emp_train.train_models()
        except Exception:
            self.assertTrue(False)

    def test_different_model(self):
        price_out_knn = self.emp_test.test_model("2016-12-12", "KNN")
        self.assertIsNotNone(price_out_knn)
        self.assertTrue(len(price_out_knn), 24)

    def test_output_len(self):
        price_out = self.emp_test.test_model("2016-12-12", 'SVM_rbf')
        self.assertTrue(len(price_out), 24)

    def test_model_initialization(self):
        with self.assertRaises(ValueError):
            self.emp_test.train_models()

if __name__ == '__main__':
    unittest.main()
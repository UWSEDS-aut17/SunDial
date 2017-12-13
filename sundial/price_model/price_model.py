import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn import svm
from sundial.price_model.utils.file_utils import *
from sundial.price_model.utils.settings import *
from sundial.price_model.parameter_tuning import plot_pred_test_relation
from sundial.price_model.parameter_tuning import plot_predictions


REGRESSORS = {
                "SVM_rbf": svm.SVR(C=1000, gamma=0.001, kernel='rbf',
                                   epsilon=10),
                "Linear": LinearRegression(normalize=True),
                "KNN": KNeighborsRegressor(n_neighbors=8)
             }


class EnergyPriceModel():
    def __init__(self, train=False):
        self.train = train
        price_frame = pd.read_csv(PRICE_DATA_FILENAME, index_col=0)
        self.df_price_frame = price_frame.set_index("time")
        self.df_price_frame = self.df_price_frame.dropna()

    def get_train_test_data(self):
        X_price_frame = self.df_price_frame.drop('lmp_value', axis=1).\
            reset_index().drop('time', axis=1)
        Y_price_frame = self.df_price_frame['lmp_value']
        return train_test_split(X_price_frame, Y_price_frame, shuffle=False)

    def train_models(self):
        if not self.train:
            raise ValueError("Not initialized as train")

        x_train, x_test, y_train, y_test = self.get_train_test_data()

        for model_name, model in REGRESSORS.items():
            reg_model = model.fit(x_train, y_train)
            y_pred = reg_model.predict(x_test)
            print("The test score R2 for {0}: {1}".format(model_name,
                  reg_model.score(x_test, y_test)))
            print("{0} mean squared error: {1}".format(model_name,
                  np.mean((y_test - reg_model.predict(x_test)) ** 2)))

            if SAVE_PLOTS:
                target_folder = os.path.join(PLOTS_FOLDER, "final_plots")
                make_dir(target_folder)
                plot_predictions(x_test, y_test, y_pred, model_name,
                                 target_folder)
                plot_pred_test_relation(y_test, y_pred, model_name,
                                        target_folder)

            if SAVE_MODEL:
                target_folder = os.path.join(MODEL_FOLDER,
                                             "{0}.model".format(model_name))
                self.save_model(reg_model, target_folder)

    def test_model(self, test_date, model_name):
        load_path = os.path.join(MODEL_FOLDER, "{0}.model".format(model_name))
        reg_model = self.load_model(load_path)
        begin = test_date + ' 00:00:00'
        end = test_date + ' 23:00:00'
        feature_vec = self.df_price_frame.loc[begin:end].\
            drop('lmp_value', axis=1).values
        return reg_model.predict(feature_vec)

    def save_model(self, reg_model, path):
        joblib.dump(reg_model, path)

    def load_model(self, path):
        return joblib.load(path)

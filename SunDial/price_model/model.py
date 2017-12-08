import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn import svm
from utils.file_utils import *
from parameter_tuning import plot_pred_test_relation
from parameter_tuning import plot_predictions
from utils.settings import *


REGRESSORS = {
				"SVM_rbf": svm.SVR(C=1000, gamma=0.001, kernel='rbf', epsilon=10),
				"Linear": LinearRegression(normalize=True),
				"KNN": KNeighborsRegressor(n_neighbors=8)
			 }

def get_train_test_data(df_price_frame):
	df_price_frame = df_price_frame.dropna()
	X_price_frame = df_price_frame.drop('lmp_value', axis=1).reset_index().drop('time', axis=1)
	Y_price_frame = df_price_frame['lmp_value']
	return train_test_split(X_price_frame, Y_price_frame, shuffle=False)


def train_models(df_price_frame):
	x_train, x_test, y_train, y_test = get_train_test_data(df_price_frame)
	
	for model_name, model in REGRESSORS.items():
		reg_model = model.fit(x_train, y_train)
		y_pred = reg_model.predict(x_test)

		print "The test score R2 for {0}: {1}".format(model_name, reg_model.score(x_test, y_test))

		print "{0} mean squared error: {1}".format(model_name, np.mean((y_test - reg_model.predict(x_test)) ** 2))

		if SAVE_PLOTS:
			target_folder = os.path.join(PLOTS_FOLDER, "final_plots")
			make_dir(target_folder)
			plot_predictions(x_test, y_test, y_pred, model_name, target_folder)
			plot_pred_test_relation(y_test, y_pred, model_name, target_folder)

		if SAVE_MODEL:
			target_folder = os.path.join(MODEL_FOLDER, "{0}.model".format(model_name))
			save_model(reg_model, target_folder)

def save_model(reg_model, path):
	joblib.dump(reg_model, path)

def main():
	price_frame = pd.read_csv(PRICE_DATA_FILENAME, index_col=0)
	df_price_frame = price_frame.set_index("time")
	train_models(df_price_frame)

if __name__ == '__main__':
	main()
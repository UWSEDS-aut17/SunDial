import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import neighbors
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from utils.file_utils import *
import multiprocessing

PRICE_DATA_FILENAME = "../data/sm_price/processed_price.csv"
PLOTS_FOLDER = "./plots"

def get_train_test_data(df_price_frame):
	df_price_frame = df_price_frame.dropna()
	X_price_frame = df_price_frame.drop('lmp_value', axis=1).reset_index().drop('time', axis=1)
	Y_price_frame = df_price_frame['lmp_value']
	return train_test_split(X_price_frame, Y_price_frame, shuffle=False)

def tune_models(df_price_frame):
	x_train, x_test, y_train, y_test = get_train_test_data(df_price_frame)
	tune_svr(x_train, y_train, x_test, y_test)
	tune_knn(x_train, y_train, x_test, y_test)
	tune_lin_reg(x_train, y_train, x_test, y_test)

def tune_svr(x_train, y_train, x_test, y_test):
	C_range = range(1000, 3000, 1000)
	tuned_parameters = [{
		"C": C_range,
		"kernel": ["rbf"]
	}]
	svr_reg = GridSearchCV(svm.SVR(gamma=0.001, epsilon=10), param_grid=tuned_parameters, verbose=1,
						   n_jobs=multiprocessing.cpu_count())
	y_pred = svr_reg.fit(x_train, y_train).predict(x_test)

	print 'Optimum parameters epsilon and kernel for SVR: ', svr_reg.best_params_

	print("The test score R2 for SVR: ", svr_reg.score(x_test, y_test))

	print("SVR mean squared error: %.2f"
		  % np.mean((y_test - svr_reg.predict(x_test)) ** 2))

	target_folder = os.path.join(PLOTS_FOLDER, "svr")
	make_dir(target_folder)
	plot_predictions(x_test, y_test, y_pred, "svr", target_folder)
	plot_pred_test_relation(y_test, y_pred, "svr", target_folder)


def tune_knn(x_train, y_train, x_test, y_test):
	n_range = range(1, 10, 1)
	tuned_parameters = [{
		"n_neighbors": n_range
	}]
	knn_reg = GridSearchCV(neighbors.KNeighborsRegressor(), param_grid=tuned_parameters, verbose=1,
						   n_jobs=multiprocessing.cpu_count())
	y_pred = knn_reg.fit(x_train, y_train).predict(x_test)

	print 'Optimum parameters epsilon and kernel for KNN: ', knn_reg.best_params_

	print("The test score R2 for KNN: ", knn_reg.score(x_test, y_test))

	print("KNN mean squared error: %.2f"
		  % np.mean((y_test - knn_reg.predict(x_test)) ** 2))

	target_folder = os.path.join(PLOTS_FOLDER, "knn")
	make_dir(target_folder)
	plot_predictions(x_test, y_test, y_pred, "knn", target_folder)
	plot_pred_test_relation(y_test, y_pred, "knn", target_folder)


def tune_lin_reg(x_train, y_train, x_test, y_test):
	lin_reg = linear_model.LinearRegression(normalize=True)
	y_pred = lin_reg.fit(x_train, y_train).predict(x_test)

	print("The test score R2 for Lin Reg: ", lin_reg.score(x_test, y_test))

	print("Lin Reg mean squared error: %.2f"
		  % np.mean((y_test - lin_reg.predict(x_test)) ** 2))

	target_folder = os.path.join(PLOTS_FOLDER, "lin")
	make_dir(target_folder)
	plot_predictions(x_test, y_test, y_pred, "lin", target_folder)
	plot_pred_test_relation(y_test, y_pred, "lin", target_folder)


def plot_predictions(x_test, y_test, y_pred, model_name, path):
	plt.figure(figsize=(15, 7))
	plt.scatter(x_test.index, y_test, c='k', label='Observed')
	plt.plot(x_test.index, y_pred, c='r', label='Predicted')
	plt.xlabel('data')
	plt.ylabel('lmp_value')
	plt.title('model')
	plt.legend()
	plt.savefig(os.path.join(path, "{0}_predictions".format(model_name)))

def plot_pred_test_relation(y_test, y_pred, model_name, path):
	plt.figure(figsize=(6, 6))
	plt.scatter(y_test, y_test, c='k')
	plt.scatter(y_test, y_pred, c='r')
	plt.xlabel('Observed Elec. Price (MWhr)')
	plt.ylabel("Predicted Elec. Price (MWWh): $\hat{Y}_i$")
	plt.title("Energy vs Predicted Energy: $Y_i$ vs $\hat{Y}_i$")
	plt.savefig(os.path.join(path, "{0}_relation".format(model_name)))


def main():
	price_frame = pd.read_csv(PRICE_DATA_FILENAME, index_col=0)
	df_price_frame = price_frame.set_index("time")
	tune_models(df_price_frame)

if __name__ == '__main__':
	main()
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from process_data import process_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn import svm
from sklearn import grid_search
from sklearn.grid_search import GridSearchCV

REGRESSORS = {
				# "SVM_rbf": svm.SVR(C=1000, gamma=0.001, kernel='rbf', epsilon=10)
				# "Linear": LinearRegression(normalize=True),
				"KNN": KNeighborsRegressor()
			 }

DATA_ITEMS = 25
PRICE_DATA_FILENAME = "../data/sm_price/processed_price.csv"


def get_train_test_data(df_price_frame):
	df_price_frame = df_price_frame.dropna()
	X_price_frame = df_price_frame.drop('lmp_value', axis=1).reset_index().drop('time', axis=1)
	Y_price_frame = df_price_frame['lmp_value']
	return train_test_split(X_price_frame, Y_price_frame, shuffle=False)

def model(df_price_frame):
	x_train, x_test, y_train, y_test = get_train_test_data(df_price_frame)
	
	for model_name, model in REGRESSORS.items():
		# svr_reg = model.fit(x_train, y_train)
		n_range = range(1, 10, 1)
		tuned_parameters = [{"n_neighbors":n_range}]
		svr_reg = GridSearchCV(model, param_grid=tuned_parameters, verbose=1)
		y_pred = svr_reg.fit(x_train, y_train).predict(x_test)

		print("The test score R2 for SVR: ", svr_reg.score(x_test, y_test))

		print("SVR mean squared error: %.2f"
		      % np.mean((y_test - svr_reg.predict(x_test)) ** 2))

		fig = plt.figure(figsize=(15,7))
		plt.scatter(x_test.index, y_test, c='k', label='Observed')
		plt.plot(x_test.index, y_pred, c='r', label='Predicted')
		plt.xlabel('data')
		plt.ylabel('lmp_value')
		plt.title('Support Vector Regression')
		plt.legend()
		plt.show()

		fig = plt.figure(figsize=(6,6))
		plt.scatter(y_test, y_test, c='k')
		plt.scatter(y_test, y_pred, c='r')
		plt.xlabel('Observed Elec. Usage (kWh)')
		plt.ylabel("Predicted Elec. Usage (kWh): $\hat{Y}_i$")
		plt.title("Energy vs Predicted Energy: $Y_i$ vs $\hat{Y}_i$")
		plt.show()


def main():
	price_frame = pd.read_csv(PRICE_DATA_FILENAME, index_col=0)
	df_price_frame = price_frame.set_index("time")
	model(df_price_frame)

if __name__ == '__main__':
	main()
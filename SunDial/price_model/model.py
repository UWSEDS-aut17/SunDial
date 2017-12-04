import numpy as numpy
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
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPRegressor

REGRESSORS = {
				"SVM_rbf": svm.SVR(kernel='rbf', C=100, gamma=0.001),
				"Linear": LinearRegression(normalize=True),
				"KNN": KNeighborsRegressor(n_neighbors=10)
			 }

DATA_ITEMS = 25


def model(X, y):
	Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)
	
	for model_name, model in REGRESSORS.items():
		print model_name
		model.fit(Xtrain[:, 1:], ytrain)
		ypred = model.predict(Xtest[:, 1:])

		x_vals = Xtest[:, 0][:DATA_ITEMS]
		y_vals = model.predict(Xtest[:, 1:])[:DATA_ITEMS]

		score = model.score(Xtest[:, 1:], ytest)
		print score

		plt.title(model_name)
		plt.scatter(x_vals, list(ytest)[:DATA_ITEMS], color='b')
		plt.scatter(x_vals, list(y_vals), color='g')
		plt.show()

def main():
	price_data, headers = process_data()
	y = price_data[:, 0]
	x = price_data[:, 1:]
	model(x, y)

if __name__ == '__main__':
	main()
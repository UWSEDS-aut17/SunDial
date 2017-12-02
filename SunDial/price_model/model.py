import numpy as numpy
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from process_data import process_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn import svm
from sklearn.metrics import confusion_matrix


def model(X, y):
	Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)
	model = svm.SVR(kernel='rbf',C=100,gamma=.001) #LinearRegression(normalize=True)
	model.fit(Xtrain[:, 1:], ytrain)
	ypred = model.predict(Xtest[:, 1:])

	variance_score = explained_variance_score(ytest, ypred, multioutput='raw_values')
	print variance_score
	mean_squared = mean_squared_error(ytest, ypred)
	print mean_squared
	r_squared = r2_score(ytest, ypred, multioutput='raw_values')
	print r_squared

	x_vals = Xtest[:, 0]
	y_vals = model.predict(Xtest[:, 1:])

	print x_vals.shape
	# x_train

	plt.scatter(x_vals, list(ytest), color='b')
	plt.scatter(x_vals, y_vals,color='g')
	plt.show()


def main():
	price_data, headers = process_data()
	y = price_data[:, 0]
	x = price_data[:, 1:]
	model(x, y)

if __name__ == '__main__':
	main()
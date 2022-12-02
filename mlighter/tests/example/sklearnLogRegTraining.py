# Load libraries
from pandas import read_csv
import numpy as np
from sklearn.model_selection import train_test_split
import sys
from sklearn.svm import SVC 
import joblib

#byte_arr = np.array([ 0, 1000,0, 3, 0,1,0,1,200,0,-1],dtype=np.int64 ).tofile("input.bin")
#exit()
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(url, names=names)

# Split-out validation dataset
array = dataset.values
X = array[:,0:4]
y = array[:,4]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)
# Make predictions on validation dataset
model = SVC(probability=True)
model.fit(X_train, Y_train)
joblib.dump(model, "irisProb.joblib")
predictions = model.predict(X_validation)
print(predictions)


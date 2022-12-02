# Load libraries
from pandas import read_csv
import numpy as np
from sklearn.model_selection import train_test_split
import struct
import sys
from sklearn.linear_model import LogisticRegression
import afl, os
#byte_arr = np.array([ 0, 1000,0, 3, 0,1,0,1,200,0,-1],dtype=np.int64 ).tofile("input.bin")
#exit()
args = sys.argv
#print(args[0])
#print(args[1])
first=['l1', 'l2','none','elasticnet']
second=['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
third=['auto', 'ovr', 'multinomial']
inputArray=np.load(args[1])
#print(inputArray)
byte_arr = [first[inputArray[0]%len(first)],bool(inputArray[1]%2),
            float(inputArray[2])/1000.0,float(inputArray[3])/1000.0,
            bool(inputArray[4]%2), float(inputArray[5])/1000.0,
            second[inputArray[6]%len(second)],
            inputArray[7],
            third[inputArray[8]%len(third)],
            float(inputArray[9])/1000.0]

print(byte_arr)
#exit()
#byte_arr = np.array([ 'auto', 1.0,'rbf', 3, 0.0,True,False,0.001,200,False,-1])
#byte_arr.tofile("test")
#print(byte_arr.tobytes())
#f = open('input.bin', 'w+b')
#binary_format = bytearray(byte_arr)
#f.write(binary_format)
#f.close()


url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(url, names=names)

# Split-out validation dataset
array = dataset.values
X = array[:,0:4]
y = array[:,4]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)
# Make predictions on validation dataset
model = LogisticRegression(penalty=byte_arr[0],dual=byte_arr[1], tol=byte_arr[2], C=byte_arr[3] ,fit_intercept=byte_arr[4] , intercept_scaling=byte_arr[5], solver=byte_arr[6],max_iter=byte_arr[7], multi_class=byte_arr[8],l1_ratio=byte_arr[9])
#model = SVC(gamma='auto',C=1.0, kernel='rbf', degree=3, coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, verbose=False, max_iter=-1)
model.fit(X_train, Y_train)
#predictions = model.predict(X_validation)
#print(predictions)
os._exit(0)

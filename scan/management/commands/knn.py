#Con DB Iris me da precision y recall de 1 mejor q SVM y q NB, es una variable categorica con target (0,1 y 2) tipos plantas
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier

%matplotlib inline
iris = datasets.load_iris()
iris.keys()
df = pd.DataFrame(iris['data'],columns=iris['feature_names'],)
results = iris['target']
X = df
y = np.array(results)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train,y_train)
pred = knn.predict(X_test)
print(confusion_matrix(y_test,pred))
print('\n')
print(classification_report(y_test,pred))

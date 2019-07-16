from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
%matplotlib inline
iris = datasets.load_iris()
iris.keys()
df = pd.DataFrame(iris['data'],columns=iris['feature_names'])
results = iris['target']
X = df
y = np.array(results)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
dtree = DecisionTreeClassifier()
dtree.fit(X_train,y_train)
pred = dtree.predict(X_test)
print(confusion_matrix(y_test,pred))
print('\n')
print(classification_report(y_test,pred))

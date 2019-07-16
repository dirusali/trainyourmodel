#Naive Bayes implementado con GaussianNB pero es igual con BernouilliNB, CompetentNB o MultinomialNB
#Naive Bayes es un clasificador sencillo y potente, la Regresion Logistica solo lo supera cuando muestra tienda a infinito

from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

%matplotlib inline
iris = datasets.load_iris()
iris.keys()
df = pd.DataFrame(iris['data'],columns=iris['feature_names'],)
results = iris['target']
X = df
y = np.array(results)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
gnb = GaussianNB()
gnb.fit(X_train,y_train)
pred = gnb.predict(X_test)
print(confusion_matrix(y_test,pred))
print('\n')
print(classification_report(y_test,pred))

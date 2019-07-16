# Decision trees: lo que hace es calcular info ganada en cada paso, hasta q no se gana ganada => entropia = 0, paro la rama
# Es como dividir el dataset en trozos para ver de q está hecho hasta q los trozos son homogeneos, no hay q dividr +
# Construimos el arbol de posibilidades y elegimos el atributo q más info aporta como el nodo inicial
# Repetimos el proceso diviendo desde el inicial hasta q cada rama queda en 0 
# Es forma util para clasificar los algoritmos de mi web, de manera q llego al q hay q usar con el minimo numero de preguntas

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

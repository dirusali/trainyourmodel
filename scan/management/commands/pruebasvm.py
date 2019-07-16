#Algoritmo para predecir variables categóricas (SIvsNO),(+,-),(Azul,rojo), podriamos crear (x,y,z,t) clusters con Kmeans y con SVM predecir si los elementos de una muestra caen en una u otra categoria
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
%matplotlib inline
import csv
infile = open('breast_cancer.csv', 'r', errors = 'ignore')                                                                                                     
reader = csv.reader(infile, delimiter=',')  
lista = []
for i in reader:
    lista.append(i)
infile.close()  
long = len(lista[0])
header = lista[0][0:(long-1)]
corte = len(lista) - 1
lista = lista[1:corte]
results = []
for i in lista:
    x = i[long-1]
    results.append(float(x))
newlist=[]
for i in lista:
    numbers = i[0:(long-1)]
    numbers = [ float(n) for n in numbers ]
    newlist.append(numbers)    
df = pd.DataFrame(np.array(newlist),columns=np.array(header))
for v in header:
    column = df[v]
    m = np.median(column)
    count=-1
    print('VAMOS CON LA COLUMNA %s' % v)
    for i in column: 
        count+=1
        if i > 10*m:
            df.set_value(count, v, m)
            print('sustituyendo valor %s, ahora queda %s y deberia ser %s' % (i,df[v][count],m))
        if i < (m/10):
            df.set_value(count, v, m)
            print('sustituyendo valor %s, ahora queda %s y deberia ser %s' % (i,df[v][count], m))
X = df
y = np.array(results)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
param_grid = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
grid = GridSearchCV(SVC(),param_grid,verbose=3)
grid.fit(X_train,y_train)
grid_predictions = grid.predict(X_test)
print(confusion_matrix(y_test,grid_predictions))
print('\n')
print(classification_report(y_test,grid_predictions))
    

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
df_feat = pd.DataFrame(np.array(newlist),columns=np.array(header))
X = df_feat
y = np.array(results)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
param_grid = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
grid = GridSearchCV(SVC(),param_grid,verbose=3)
grid.fit(X_train,y_train)
grid_predictions = grid.predict(X_test)
print(confusion_matrix(y_test,grid_predictions))
print('\n')
print(classification_report(y_test,grid_predictions))
    

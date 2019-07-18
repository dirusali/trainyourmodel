#EN ESTE CASO PREDECIMOS VBLE CATEGORICA X ESO FINAL_PRE ES 0,1,2 (TIPOS PLANTAS) Y ELEGIMOS DNNClassifier Q PODRIA SER REGRESSOR EN OTRO CASO
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.datasets import load_iris
iris = load_iris()
import tensorflow as tf
features = []
for i in iris['feature_names']:
    i=i.replace(" ","")
    features.append(i)
features.append('target')
#df = pd.DataFrame(iris['data'],columns=features)
data = []
for i in iris['data']:
    i=list(i)
    data.append(i)
count=-1
for i in range(150):
    count+=1
    data[count].append(target[count])
columnas=[]
for i in features:
    i = i[0:6]
    columnas.append(i)
columnas  
df = pd.DataFrame(data,columns=columnas)
y = df['target']
X= df.drop(['target'],axis=1)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
feat_cols = []
for col in X.columns:
    feat_cols.append(tf.feature_column.numeric_column(col))
input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train,batch_size=10,num_epochs=5,shuffle=True)
classifier=tf.estimator.DNNClassifier(hidden_units=[10,20,10],n_classes=3,feature_columns=feat_cols)
classifier.train(input_fn=input_func,steps=50)
pred = tf.estimator.inputs.pandas_input_fn(x=X_test,batch_size=len(X_test),shuffle=False)
predictions=list(classifier.predict(input_fn=pred))
final_preds = []
for i in predictions:
    final_preds.append(i['class_ids'][0])

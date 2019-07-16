# Este Algoritmo sirve para clasificar RESULTADOS ETIKETANDOLOS: en este caso se que hay dos clusters: hombre y mujer
# Si no conozco los datos de una muestra puedo dividir en tantos clusters como quiera y clasificarlos asi

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
%matplotlib inline
file = 'path-to-file' #aqui uso sexo.csv que tra labels 1 y 0 para hombre y mujer y asi puedo comparar resultado con mis labels
df = pd.read_csv('sexo.csv')
long = len(df.head(0)) - 1
header = list(df)[0:long]
labels = header[long]
results = df[labels]
data = df.drop('resultados',axis=1,inplace=True)
df = df.values
data = (df,resultados) # necesita una tuple con dos arrays, el input y los labels xq los kiero pintar y comparar
kmeans.fit(df)
kmeans.cluster_centers_
kmeans.labels_
fig, (ax1,ax2) = plt.subplots(1,2, sharey=True,figsize=(10,6))
ax1.set_title('Original')
ax1.scatter(data[0][:,0],data[0][:,1],c=resultados)
ax2.set_title('Model')
ax2.scatter(data[0][:,0],data[0][:,1],c=kmeans.labels_)

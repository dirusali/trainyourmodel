#la varianza es lo q cambia y cuando muevo una unidad de x
#el coef de corr es r y determinacion es el r2, el r2 ajustado elimina el efecto de variables q no aportan nada al modelo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
from sklearn.datasets import load_boston 
from sklearn import metrics
boston = load_boston()
df = pd.DataFrame(boston['data'],columns=boston['feature_names'])
price = boston['target']
X = df
y = price
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4,random_state=101) 
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train,y_train)
pred = lm.predict(X_test)
plt.scatter(y_test,pred)
print('MAE:', metrics.mean_absolute_error(y_test,pred))
print('MAE:', metrics.mean_squared_error(y_test,pred))
print('MAE:', np.sqrt(metrics.mean_squared_error(y_test,pred)))

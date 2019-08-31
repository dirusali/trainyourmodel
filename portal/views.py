# This Python file uses the following encoding in format utf-8
import plotly
import plotly.express as px
import plotly.graph_objects as go

import io
import csv
from io import BytesIO
import base64
import functools
import operator
import random
import unicodedata
import datetime
import pandas as pd
import seaborn as sns
import numpy as np
from efficient_apriori import apriori

from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop

from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Count
from django.shortcuts import redirect

from portal.models import Subscribe
#from portal.utils import SendSubscribeMail, round_next_down, round_next_up

from el_pagination.views import AjaxListView
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static
 
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={}
        context['is_home'] = True
        context['lazyjs'] = True
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request, 'portal.html', context)


class ContactoView(View):

    def get(self, request, *args, **kwargs):
        context={}
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        return render(request, 'contacto.html', context)


class PrivacidadView(View):

     def get(self, request, *args, **kwargs):
        context={}
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request, 'priv.html', context)


       
def contacto(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email_contacto')
        message = request.POST.get('message')
        
        body = render_to_string(
            'email_content.html', {
                'name': name,
                'email': email,
                'message': message,
            },
        )

        if name and message and email:
            try:
                #email_message.send()
                send_mail('Feedmedata :: Formulario Web', body, 'dirusali@gmail.com', ['dirusali@gmail.com'])
                send_mail('Feedmedata', 'Your email was sent, I will try to respond asap', 'dirusali@gmail.com', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/message-sent/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Please check you filled all fields correctly.')
    else:
        context={}
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno
        
        return render(request, 'contacto.html', context)      


		
def successView(request):
    context={}
    context['is_home'] = True
    context['lazyjs'] = False
    context['valoracionesjs'] = False
    context['valoracionesTiendajs'] = False
    context['normal_footer_cat'] = True

    return render(request, 'success.html', context)
       
class FuncionaView(View):

    def get(self, request, *args, **kwargs):
        context={}
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request, 'funciona.html', context)
	
class NeuralView(View):

    def get(self, request, *args, **kwargs):
        context={}
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request, 'nn.html', context)


class CondicionesView(View):

     def get(self, request, *args, **kwargs):
        context={}
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request, 'terms.html', context)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_qs = Subscribe.objects.filter(email_id=email)
        if email_qs.exists() or len(email)==0:
            data = {"status" : "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(email_id=email)
            SendSubscribeMail(email) # Send the Mail, Class available in utils.py
    return HttpResponse("/")

def successView(request):
        context={}
        context['is_home'] = True
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request, 'success.html', context)

def neural(request):	
	if request.method == "POST":
	    file = request.FILES['file']
	    df = pd.read_csv(file)
	    df_target = df
	    lon = len(list(df.head(0)))
	    dim = lon -1	
	    header = list(df[0:lon])
	    target = header[dim]
	    y = np.array(df[target])
	    df.drop(target,axis=1,inplace=True)
	    X = df.values
	    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=101) 
	    graph_div = ''
	    pred = ''
	    red = request.POST['red']
	    dense = int(request.POST['epoch'])	
	    epoch = int(request.POST['epoch'])
	    batch = int(request.POST['batch'])
	    nodes = int(request.POST['categories'])
	    if red == 'Binary Crossentropy':
			    model = Sequential()
			    model.add(Dense(dense, input_dim=dim, activation='relu'))
			    model.add(Dense(dim-1, activation='relu'))
			    model.add(Dense(1, activation='sigmoid'))
			    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
			    model.fit(x=X,y=y,batch_size=batch, epochs=epoch,shuffle=True)
			    _, accuracy = model.evaluate(X, y)
			    accu = print('Accuracy: %.2f' % (accuracy*100))
			    context = {'accu': accu}           
			    return render(request, "neural.html", context)
	    if red == 'Mean Squared Error':
			    model = Sequential()
			    model.add(Dense(dense, input_dim=dim, activation='relu'))
			    model.add(Dense(1, activation='linear'))
			    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
			    model.fit(x=X,y=y,batch_size=batch, epochs=epoch,shuffle=True)
			    pred = model.predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse = np.sqrt(metrics.mean_squared_error(y_test,pred))
			    fig = go.Figure(data=go.Scatter(x=y_test, y=pred, mode='markers'))
			    fig.update_xaxes(title="Test Sample")
			    fig.update_yaxes(title="Predictions")
			    fig.update_layout(autosize=False, width=800,height=500)
			    scatter = plotly.offline.plot(fig, auto_open = False, output_type="div")	
			    context = {'scatter': scatter, 'mae': mae, 'mse': mse, 'rmse': rmse}           
			    return render(request, "scatter.html", context)
	    if red == 'Multiclass Crossentropy': 
			    model = Sequential() 
			    model.add(Dense(dense, input_dim=dim, activation='relu'))
			    model.add(Dense(nodes, activation='softmax'))
			    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
			    model.fit(x=X,y=y,batch_size=batch, epochs=epoch,shuffle=True)
			    _, accuracy = model.evaluate(X, y)
			    accu = print('Accuracy: %.2f' % (accuracy*100))
			    context = {'accu': accu}           
			    return render(request, "neural.html", context)
				  	       		      
			       	
def upload_csv(request):	
	if request.method == "POST":
	    csv = request.FILES['csv_file']
	    df = pd.read_csv(csv)
	    df_target = df
	    lon = len(list(df.head(0)))
	    header = list(df[0:lon])
	    target = header[lon-1]
	    y = np.array(df[target])
	    df.drop(target,axis=1,inplace=True)
	    X = df.values
	    Z = X
	    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=101) 
	    graph_div = ''
	    pred = ''
	    algo = request.POST['algoritmo']	
	    grafica = request.POST['graficas']
	    cate = request.POST['categorical']	
	    clasi = request.POST['clasi']
	    elbow = request.POST['elbow']	
	    if request.POST['submit'] == '_plot': 
	        if grafica == "scatter":
		        fig = px.scatter_matrix(df_target)
		        graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
		        context = {'graph_div': graph_div}
		        return render (request, "plottings.html", context)
	    if request.POST['submit'] == '_cate':
		    if cate == 'apriori':
			    file = request.FILES['csv_file']
			    df = pd.read_csv(file)
			    transactions = []
			    header = list(df.head(0))
			    transactions.append(list(header))
			    for i in range(0, len(df)):
				    a = list(df.iloc[i])
				    transactions.append(a)
			    itemsets, rules = apriori(transactions, min_support=0.2,  min_confidence=1)
			    context = {'rules': rules}           	  
			    return render(request, "apriori.html", context)			  
	    if request.POST['submit'] == '_unsuper':
		    if 2 > 1:
			    Nc = range(1, 20)
			    kmeans = [KMeans(n_clusters=i) for i in Nc]
			    score = [kmeans[i].fit(Z).score(Z) for i in range(len(kmeans))]
			    fig = go.Figure(data=go.Scatter(y=score, x=list(Nc), mode='markers'))
			    fig.update_xaxes(title="Number of Clusters")
			    fig.update_yaxes(title="Error")
			    fig.update_layout(autosize=False, width=800,height=500)
			    graph = plotly.offline.plot(fig, auto_open = False, output_type="div")           
			    nclusters = int(request.POST['clusters'])
			    kmeans = KMeans(n_clusters=nclusters)
			    model = kmeans.fit(Z)
			    labels = kmeans.labels_
			    context = {'graph': graph, 'labels': labels}           
			    return render(request, "kmeans.html", context)					
	    if request.POST['submit'] == '_super': 	
		    if algo == 'Linear Regression':
			    lm = LinearRegression()
			    model = lm.fit(X_train,y_train)
			    pred = lm.predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse = np.sqrt(metrics.mean_squared_error(y_test,pred))
			    fig = go.Figure(data=go.Scatter(x=y_test, y=pred, mode='markers'))
			    fig.update_xaxes(title="Test Sample")
			    fig.update_yaxes(title="Predictions")
			    fig.update_layout(autosize=False, width=800,height=500)
			    scatter = plotly.offline.plot(fig, auto_open = False, output_type="div")	
			    context = {'scatter': scatter, 'mae': mae, 'mse': mse, 'rmse': rmse}           
			    return render(request, "scatter.html", context)	
		    if algo == 'Support Vector Machine':
			    param_grid = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
			    grid = GridSearchCV(SVC(),param_grid,verbose=3)
			    model = grid.fit(X_train,y_train)
			    pred = grid.predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse = np.sqrt(metrics.mean_squared_error(y_test,pred))
			    matrix = print(confusion_matrix(y_test,pred))
			    report = print(classification_report(y_test,pred))
		    if algo == 'K-Nearest Neighbor':
			    knn = KNeighborsClassifier(n_neighbors=1)
			    model = knn.fit(X_train,y_train)
			    pred = knn.predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse= np.sqrt(metrics.mean_squared_error(y_test,pred))
			    matrix = confusion_matrix(y_test,pred)
			    report = classification_report(y_test,pred)	
		    if algo == 'Naive Bayes':
			    gnb = GaussianNB()
			    pred = gnb.fit(X_train, y_train).predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse = np.sqrt(metrics.mean_squared_error(y_test,pred))
			    matrix = confusion_matrix(y_test,pred)
			    report = classification_report(y_test,pred)	
		    if algo == 'Decision Trees':
			    dtree = DecisionTreeClassifier()
			    model = dtree.fit(X_train,y_train)
			    pred = dtree.predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse = np.sqrt(metrics.mean_squared_error(y_test,pred))
			    matrix = confusion_matrix(y_test,pred)
			    report = classification_report(y_test,pred)
		    if algo == 'Random Forest':
			    forest = RandomForestClassifier(n_estimators=200)
			    model = forest.fit(X_train,y_train)
			    pred = forest.predict(X_test)
			    mae = metrics.mean_absolute_error(y_test,pred)
			    mse = metrics.mean_squared_error(y_test,pred)
			    rmse = np.sqrt(metrics.mean_squared_error(y_test,pred))
			    matrix = confusion_matrix(y_test,pred)	
			    report = classification_report(y_test,pred)		
		    context = {'matrix00': matrix[0][0], 'matrix01': matrix[0][1], 'matrix10': matrix[1][0], 'matrix11': matrix[1][1], 'mae': mae, 'mse': mse, 'rmse': rmse, 'f1': report[0:52], 'f2': report[54:106], 'f3': report[107:159], 'f4': report[160:213]}           
		    return render(request, "upload_csv.html", context)	
	    
 	
	
	


 

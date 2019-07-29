# This Python file uses the following encoding in format utf-8
import functools
import operator
import random
import unicodedata
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import csv, io
from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Count
#from rest_framework.permissions import IsAdminUser
from django.shortcuts import redirect

from portal.models import Subscribe
#from portal.utils import SendSubscribeMail, round_next_down, round_next_up

from el_pagination.views import AjaxListView
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static
 
def index(request):
    my_dict = {'insert_me':"hello, I am from views"}
    return render(request,'index.html',context=my_dict)
  

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
                send_mail('The Best 5 :: Formulario Web', body, 'admin@thebest5.es', ['admin@thebest5.es'])
                send_mail('The Best 5', 'Buenos días. Hemos recibido tu mensaje correctamente. Recibirás una respuesta lo antes posible.', 'admin@thebest5.es', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/mensaje-enviado/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Asegúrate de que has rellenado correctamente los campos.')
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



def data_target(documento):  	
        reader = csv.reader(documento, delimiter=',')  
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
        variables = [df,results]				      
        return variables

def LM(df,results):
    X = df
    y = price
    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4,random_state=101) 
    from sklearn.linear_model import LinearRegression
    lm = LinearRegression()
    lm.fit(X_train,y_train)
    pred = lm.predict(X_test)
    plot = plt.scatter(y_test,pred)
    #a = print('MAE:', metrics.mean_absolute_error(y_test,pred))
    #b = print('MAE:', metrics.mean_squared_error(y_test,pred))
    #c = print('MAE:', np.sqrt(metrics.mean_squared_error(y_test,pred)))	  
    return plot	


def upload_csv(request):
	if "POST" == request.method:
	    try:
	        infile = request.FILES["csv_file"]
	        reader = csv.reader(infile, delimiter=',') 
		decoded = io.stringIO(reader)
	        data = {'results': decoded}
	    except Exception as e:
	        print(e)	
	return render(request, "upload_csv.html", context=data)


def SVM(df,results):
    X = df
    y= np.array(results)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
    param_grid = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
    grid = GridSearchCV(SVC(),param_grid,verbose=3)
    grid.fit(X_train,y_train)
    grid_predictions = grid.predict(X_test)
    matrix = confusion_matrix(y_test,grid_predictions)
    report = classification_report(y_test,grid_predictions)
    return (matrix,report) 	
	
	
def NB(df,results):
    X = df
    y = np.array(results)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
    gnb = GaussianNB()
    gnb.fit(X_train,y_train)
    pred = gnb.predict(X_test)
    matrix = confusion_matrix(y_test,pred)
    report = classification_report(y_test,pred)	
    return (matrix,report)

	
 
def KNN(df,results):
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
    a = ax1.set_title('Original')
    b= ax1.scatter(data[0][:,0],data[0][:,1],c=resultados)
    c = ax2.set_title('Model')
    d = ax2.scatter(data[0][:,0],data[0][:,1],c=kmeans.labels_)	
    return d

def dtree(df,results):
    X = df
    y = np.array(results)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
    dtree = DecisionTreeClassifier()
    dtree.fit(X_train,y_train)
    pred = dtree.predict(X_test)
    a= print(confusion_matrix(y_test,pred))
    c = print(classification_report(y_test,pred))	 
    return(a,c)	      
	      	  
def kmeans(X,y):
    X = df
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
    a = fig, (ax1,ax2) = plt.subplots(1,2, sharey=True,figsize=(10,6))
    b = ax1.set_title('Original')
    c= ax1.scatter(data[0][:,0],data[0][:,1],c=resultados)
    d = ax2.set_title('Model')
    e = ax2.scatter(data[0][:,0],data[0][:,1],c=kmeans.labels_)
    return e	      
	      
	      

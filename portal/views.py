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

def upload_csv(request):
	data = {}
	if "POST" == request.method:
		return render(request, "portal/upload_csv.html", data)
	try:
	    csv_file = request.FILES["csv_file"]
	    if not csv_file.name.endswith('.csv'):
	        messages.error(request,'File is not CSV type')
		return HttpResponseRedirect(reverse("portal:upload_csv"))

	     df = pd.read_csv(csv_file)
	     return df

	except Exception as e:
	    print(e)

	return HttpResponseRedirect(reverse("portal:upload_csv"))


 This Python file uses the following encoding in format utf-8
import functools
import operator
import random
import unicodedata
import datetime

from django.template.loader import get_template, render_to_string
from clever_selects.views import ChainedSelectChoicesView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Count
from rest_framework.permissions import IsAdminUser
from django.shortcuts import redirect

from portal.models import Subscribe
from portal.utils import SendSubscribeMail, round_next_down, round_next_up
from scan.models import SearchTag, SearchTagCounter, RatedProduct, ProductPurchaseOption, CategoryImage, Article, Opinion, Shop, OpinionShop
from scan.serializers import SearchTagSearializer
from portal.models import Subscribe

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import timedelta
from el_pagination.views import AjaxListView

from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError

from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static

from django.core.mail import send_mail, BadHeaderError, EmailMessage

from .forms import NameForm

def error404(request):
    context = {}
    #context = {"project_name":"web"}

    context['category_images'] = CategoryImage.objects.all().order_by('name')
    context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
    context['is_home'] = False
    context['lazyjs'] = False
    context['valoracionesjs'] = False
    context['valoracionesTiendajs'] = False
    context['normal_footer_cat'] = True
    current_anno = datetime.datetime.now().strftime('%Y')
    context['current_anno'] = current_anno
    return render(request, '404.html', context)

def error500(request):
    context = {}
    context['category_images'] = CategoryImage.objects.all().order_by('name')
    context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
    context['is_home'] = False
    context['lazyjs'] = False
    context['valoracionesjs'] = False
    context['valoracionesTiendajs'] = False
    context['normal_footer_cat'] = True
    current_anno = datetime.datetime.now().strftime('%Y')
    context['current_anno'] = current_anno



def formatea(p):
    p = unicodedata.normalize("NFKD", p).encode("ascii","ignore").decode("ascii")
    if p[-2:].lower() == 'es':
        p = p[:-2]
    if p[-1:].lower() == 's':
        p = p[:-1] 
    return p    

def unchain(cadena):
    cadena = cadena.split(':')
    precio = cadena[0]
    time = cadena[1]
    precio = precio[2:]
    precio = precio[:-2]
    precio = float(precio)
    precio = str(precio) + '1'
    precio = float(precio)
    time = time[:-1]
    time = time[:-2] + '000'
    time = int(time)
    par = [time,precio]
    return par
    

def convertlist(pricelist):
    lista = []
    for i in pricelist:
        x = unchain(i)
        lista.append(x)
    return lista


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
        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
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

        # Get most searched topics
        last_month = today -  datetime.timedelta(30)
        topics = [x['tag'] for x in SearchTagCounter.objects.filter(hit__gte=last_month).values('tag').annotate(total=Count('tag')).order_by('-total')[:50]]
        context['searched'] = SearchTag.active_objects.filter(id__in=topics).extra(where=["LENGTH(tag) - LENGTH(REPLACE(tag, ' ', ''))+1 < %s"], params=[3])[:5]

        # Modificación para cargar todas las categorías en Home
        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = True
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno

        return render(request, 'success.html', context)

    
def get_search_tags_from_search_text(text):
    
    results = []
    q = SearchTag.active_objects.filter(is_valid=True)
    clean_text = text.lower()
    bad_phrases = ['the best5', 'the best 5', 'thebest5', 'mejores 5', 'mejores cinco', 'los mejores cinco', '5 mejores' ,'los 5 mejores', 'los cinco mejores','las 5 mejores', 'las cinco mejores', 'las mejores', 'los mejores', 'el mejor', 'la mejor', 'the best', 'the best five', 'the best 5']
    
    for w in bad_phrases:
        if w in clean_text:
            clean_text = clean_text.replace(w, '')
    
    words_list = clean_text.split()
    bad_words = ['mejor', 'mejores', 'el', 'los', 'la', 'las', 'de', 'para', '5']
    
    for w in words_list:
        if w in bad_words:
            words_list.remove(w)
    
    singulares = []
    
    for w in words_list:
        f = formatea(w)
        singulares.append(f)    
    
    final = []
    
    if words_list == ['go', 'pro']:
        final = SearchTag.active_objects.filter(tag='gopro')
    if words_list == ['camaras', 'go', 'pro']:
        final = SearchTag.active_objects.filter(tag='gopro')    
 
    if 'regalos' in words_list:
        if 'chicos' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_him=True)
        if 'hombres' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_him=True) 
        if 'chico' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_him=True)
        if 'hombre' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_him=True)     
        if 'mujer' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_her=True)
        if 'mujeres' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_her=True)
        if 'chica' in words_list: 
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_her=True) 
        if 'chicas' in words_list:
            final = SearchTag.active_objects.filter(is_valid=True).filter(for_her=True) 
        if ['regalos'] == words_list:
            final = SearchTag.active_objects.filter(Q(for_him=True) | Q(for_her=True))    
     
        
    if len(words_list) > 0:
        first_word = singulares[0]
        search_tags = q.filter(tag__icontains=first_word) 
        alias = q.filter(alias__icontains=first_word) 
        if len(search_tags) == 0 and first_word[-1:].lower() == 's' and len(first_word) > 2:
            first_word_singular = first_word[:-2] 
            search_tags = q.filter(tag__icontains=first_word_singular)
            alias = q.filter(alias__icontains=first_word_singular)                                                        
        if len(search_tags) == 0:
            search_tags = q.filter(best5_links__brand__in=words_list)
        
        marcas =  q.filter(best5_links__brand=singulares[0])
        for i in marcas:
            results.append(i)
        for i in search_tags:
            results.append(i)
        
        results =  order_results(results,singulares)
        alias_final = order_results(alias,singulares)
        for i in alias_final:
            if i not in results:
                results.append(i)
        
        if len(results) == 0: 
            if len(words_list) > 1:
                second_word = singulares[1]
                search_tags = q.filter(tag__icontains=second_word) 
                alias = q.filter(alias__icontains=second_word) 
                if len(search_tags) == 0 and second_word[-1:].lower() == 's' and len(second_word) > 2:
                    second_word_singular = second_word[:-2] 
                    search_tags = q.filter(tag__icontains=second_word_singular)
                    alias = q.filter(alias__icontains=second_word_singular)                                                        
                if len(search_tags) == 0:
                    search_tags = q.filter(best5_links__brand__in=words_list)
                results =  order_results(search_tags,singulares)
                alias_final = order_results(alias,singulares)
                for i in alias_final:
                    if i not in results:
                        results.append(i)
            else:
                results = results
        
        if len(words_list) > 1:
            other_words = words_list[1:]
            resultados = []
            nametags = []
            aliases = []
            name = SearchTag.objects.filter(is_active=True).filter(tag__icontains=first_word)
            brand = SearchTag.objects.filter(is_active=True).filter(best5_links__brand__in=other_words)
            inter = set(name)&set(brand)
            for word in other_words:
                if len(word) > 3:
                    nametags+=name.filter(tag__icontains=word)
            for i in inter:
                if i not in nametags:
                    nametags.append(i)
            #resultados = order_results(nametags,singulares)
            namealias = SearchTag.objects.filter(is_active=True).filter(alias__icontains=first_word)
            for word in other_words:
                if len(word) > 3:  
                    aliases+= namealias.filter(alias__icontains=word)
           # resultados_alias = order_results(aliases,singulares)
            for r in aliases:
                if r not in nametags:
                    nametags.append(r)
            resultados = order_results(nametags,singulares)     
            if len(resultados) > 0:
                results = resultados
    
    if final:
        return final
    else:
        return results
 

def order_results(search_tags, singulares):
    lista = []
    words = [] 
    dic = {} 
    ordenados = []
    for tag in search_tags:
        lista.append(tag.tag)
    for i in lista:
        sinonimos = []
        palabras = i.lower().split()
        for p in palabras:
            x = formatea(p) 
            sinonimos.append(x)    
        s = set(singulares)&set(sinonimos)
        rate = len(s)/len(palabras)
        dic[i] = rate
    ordered = sorted(dic, key=dic.get, reverse=True)    
    for w in ordered:
        p = w.lower().split()[0]
        palabra = formatea(p)
        if palabra == singulares[0]:
            words.append(w)
    for i in ordered:
        if i not in words:
            words.append(i)
    for i in words:
        st = SearchTag.active_objects.get(tag=i)
        ordenados.append(st)
    return ordenados  


# This view is called for autocompletion while user in writting in search box
class SearchTagApi(APIView):

    def get(self, request, format=None):
        query = str(request.GET.get('q'))
        # Old implementation searches only for tags containing all the words in search text
        #search_tags = SearchTag.active_objects.filter(is_valid=True).filter(Q(tag__icontains=query) | Q(alias__icontains=query)).order_by('-rated_reviews')
        search_tags = get_search_tags_from_search_text(query)
        serializer = SearchTagSearializer(search_tags, many=True)
        return Response(serializer.data)


# This view is called when the user searchs and press intro
class SearchTagView(AjaxListView):

    context_object_name = "tag_list"
    template_name = "tag_list.html"
    page_template='tag_list_page.html'

    def get_queryset(self):
        query = str(self.request.GET.get('q'))
        # Old implementation searches only for tags containing all the words in search text
        #return SearchTag.active_objects.filter(is_valid=True).filter(Q(tag__icontains=query) | Q(alias__icontains=query)).order_by('-rated_reviews')
        return get_search_tags_from_search_text(query)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category_images'] = CategoryImage.objects.all().order_by('name')
        data['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        data['is_search'] = True
        data['tag'] = str(self.request.GET.get('q'))
        data['busqueda'] = str(self.request.GET.get('q'))
        current_anno = datetime.datetime.now().strftime('%Y')
        data['current_anno'] = current_anno
        data['is_home'] = False
        data['lazyjs'] = True
        data['valoracionesjs'] = False
        data['valoracionesTiendajs'] = False

        return data


class HomeView(View):

    def get(self, request, *args, **kwargs):
        context={}

        # Get most searched topics
        last_month = today - timedelta(days=30)
        topics = [x['tag'] for x in SearchTagCounter.objects.filter(hit__gte=last_month).values('tag').annotate(total=Count('tag')).order_by('-total')[:50]]
        context['searched'] = SearchTag.active_objects.filter(id__in=topics).extra(where=["LENGTH(tag) - LENGTH(REPLACE(tag, ' ', ''))+1 < %s"], params=[3])[:5]

        # Get promoted categories
        # 
        # context['promoted'] = SearchTag.active_objects.filter(is_promoted=True)
        #context['categories'] = list(context['promoted'])[:6]
        # Modificación para cargar todas las categorías en Home
        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = True
        context['lazyjs'] = True
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno

        return render(request, 'portal.html', context)


class FuncionaView(View):

    def get(self, request, *args, **kwargs):
        context={}

        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno

        return render(request, 'funciona.html', context)


class ContactoView(View):

    def get(self, request, *args, **kwargs):
        context={}

        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno
        return render(request, 'contacto.html', context)



class CondicionesView(View):

     def get(self, request, *args, **kwargs):
        context={}

        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno

        return render(request, 'terms.html', context)


class PrivacidadView(View):

     def get(self, request, *args, **kwargs):
        context={}

        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno

        return render(request, 'priv.html', context)



                       

class SearchTagCategoriesDetail(AjaxListView):

    context_object_name = "tag_list"
    template_name = "tag_list.html"
    page_template = 'tag_list_page.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return SearchTag.active_objects.filter(category_slug=slug).filter(is_valid=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tag = SearchTag.active_objects.filter(category_slug=self.kwargs.get('slug')).first().category

        category_image = CategoryImage.objects.filter(name=tag).first()
        data['category_image'] = category_image
        data['tag'] = tag
        data['category_images'] = CategoryImage.objects.all().order_by('name')
        data['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        data['is_home'] = False
        data['lazyjs'] = True
        data['valoracionesjs'] = False
        data['valoracionesTiendajs'] = False
        data['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        data['current_anno'] = current_anno

        active_category_slug = self.kwargs.get('slug')
        related_links = []

        for related_link in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True):
            related_links.append(related_link)
        data['related_links'] = related_links

        return data







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





class AjaxTagProductsView(IsAdminUser, ChainedSelectChoicesView):
    def get_child_set(self):
        # Return the best 5 products related to the search tag
        products = RatedProduct.objects.filter(searchtag__id=self.parent_value, active=True).order_by('-title')
        return products
    

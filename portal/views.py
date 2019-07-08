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

today = datetime.datetime.today()

def format_date(date):
    newdate = date.split('-')
    day = newdate[0]
    month = newdate[1]
    year = newdate[2]
    
    if month == '1':
        mes = 'Jan'
    if month == '2':
        mes = 'Feb'
    if month == '3':
        mes = 'Mar'
    if month == '4':
        mes = 'Apr'
    if month == '5':
        mes = 'May'
    if month == '6':
        mes = 'Jun'
    if month == '7':
        mes = 'Jul'
    if month == '8':
        mes = 'Aug'
    if month == '9':
        mes = 'Sep'
    if month == '10':
        mes = 'Oct'
    if month == '11':
        mes = 'Nov'
    if month == '12':
        mes = 'Dec'    
    
    newdate = ('%s %s %s' % (day,mes,year))

    return newdate

def date_today():
    year = today.year
    month = today.month
    day = today.day
    fecha = '%s-%s-%s' % (day,month,year)
    return fecha

def monthago():
    monthago = today -  datetime.timedelta(30)
    year = monthago.year
    month = monthago.month
    day = monthago.day
    fecha = '%s-%s-%s' % (day,month,year)
    return fecha

def threeago():
    threeago = today -  datetime.timedelta(3*365/12)
    year = threeago.year
    month = threeago.month
    day = threeago.day
    fecha = '%s-%s-%s' % (day,month,year)
    return fecha

def sixago():
    sixago = today -  datetime.timedelta(6*365/12)
    year = sixago.year
    month = sixago.month
    day = sixago.day
    fecha = '%s-%s-%s' % (day,month,year)
    return fecha

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
    
def successRegistroTiendaView(request):
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

        return render(request, 'success-registro-tienda.html', context)
    
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


class TiendasView(View):

    def get(self, request, *args, **kwargs):
        context={}

        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['shops'] = Shop.objects.all().filter(active=True).order_by('shop_name')
        context['is_home'] = False
        context['lazyjs'] = True
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno

        return render(request, 'tiendas.html', context)


class TiendasDetail(DetailView):

    template_name = "ficha_tienda.html"    

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Shop.objects.filter(slug=slug).filter(active=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        shop = Shop.objects.filter(active=True).filter(slug=self.kwargs.get('slug')).first()

        opiniones = []
        hay_opiniones = False
        opinions = shop.opinionshop_set.all()
        media_rating=0
        cont=0
        for op in opinions:
            if op.valid == True:
                cont+=1
                media_rating += float(op.rating)
                opiniones.append(op)
        
        if len(opiniones) > 0:
            shop.rating = media_rating / int(cont)
            hay_opiniones = True
        else:
            shop.rating = 0
    
        shop.rating = str(shop.rating)
        data['rating'] = shop.rating.replace(",",".")
        data['opiniones'] = opiniones
        data['shop'] = shop
        data['category_images'] = CategoryImage.objects.all().order_by('name')
        data['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        data['is_home'] = False
        data['lazyjs'] = False
        data['valoracionesjs'] = False
        data['valoracionesTiendajs'] = True
        data['normal_footer_cat'] = True
        current_anno = datetime.datetime.now().strftime('%Y')
        data['current_anno'] = current_anno
        data['hay_opiniones'] = hay_opiniones
        #Set page canonical url
        canonical = 'https://' + self.request.get_host() + self.request.path
        data['canonical'] = canonical

        return data

class FaqView(View):

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

        return render(request, 'faq.html', context)

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


class SearchTagDetail(DetailView):
    queryset = SearchTag.active_objects.all()
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(SearchTagDetail, self).get_context_data(**kwargs)
        active_category=''
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = True
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = False

        if context['searchtag'].is_valid:

            search_tag = context['searchtag']
            #category info
            active_category = context['searchtag'].category
            active_category_slug = context['searchtag'].category_slug

            #category_image = CategoryImage.objects.filter(name=active_category).first()
            #context['category_image'] = category_image

            related_links = []
            for related_link in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True).filter(female=False):
                related_links.append(related_link)

            random.shuffle(related_links)    
            context['related_links'] = related_links

            # Trim self path
            if len(search_tag.path.split(' > ')) > 0:
                base_path = ' > '.join(search_tag.path.split(' > ')[:-1])

            # Add related tags
            related_tags = []
            nodes = search_tag.related_tags
            if nodes:
                for i in nodes:
                    tags = SearchTag.objects.filter(browsenode=i)  
                    for tag in tags:
                        related_tags.append(tag)
            else:            
                for related_tag in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True).exclude(id=search_tag.id)[:50]:
                    related_tags.append(related_tag)

            random.shuffle(related_tags)  
            context['related_tags'] = related_tags

            # Add search counter
            SearchTagCounter(tag=search_tag.id).save()

            #Post Info
            article_slug = str(context['searchtag'].slug)
            article_info = Article.objects.filter(slug =search_tag.id).filter(is_ready=True).first()
            context['article_info'] = article_info

            # Get view mode: best / price1 / price2 / price3
            view_mode = self.request.GET.get('view', 'best') # Best 5 by default
            # get best price index
            best5 = context['object']
            #best5 = [x.price for x in best5.best5_links.all()]
            #context['low_price_index'] = best5.index(0.01)

            # Get 15 products ordered by ranking, best one first
            best15_products = context['object'].best5_links.all()[:15] # We take 15 products now to be able to group by price
            best15_ranked_products = sorted(best15_products, key=lambda x: x.rank, reverse=True)

            # Get max and min to normalize ranks
            ranks = [p.rank for p in best15_ranked_products if p.rank > 0]
            rank_min = 0.01
            #rank_min = float(min(ranks))
            rank_avg = float(sum(ranks)) / max(len(ranks), 1)
            # Adjust offset to show always a value greater than 8
            rank_offset = 8.0
            hay_opiniones = False
            # Select best purchase option / shop based in price
            for prod in best15_ranked_products:
                # Check if recomendations are zero, then set a value between 0.8 and 1.0
                if prod.recommend_percentage == 0:
                   prod.recommend_percentage = 0.8 + (float(random.randrange(1, 19, 1)) / float(100.0))
                # Set best product attributes
                scaled_rank = 0
                try:  # Scale
                    scaled_rank = float(prod.rank) / float(rank_avg)
                    normalized_rank = round((scaled_rank * 0.7) + float(rank_offset), 1)
                except Exception as e:  # Handle errors
                    normalized_rank = rank_offset
                # Normalize and add offset to be between 8.0 and 9.9
                if normalized_rank >= 10.0: # check just in case
                    normalized_rank = 9.9
                normalized_rank_percentaje = int(round(normalized_rank * 10.0, 0))
                prod.best_option_rank = "{0:.1f}".format(prod.rank) 
                if prod.best_option_rank == '10.0':
                    prod.best_option_rank = '10'
                prod.best_option_rank_percentaje = normalized_rank_percentaje
                prod.best_option_price = prod.price
                prod.best_option_currency = 'EUR'
                prod.best_option_old_price = prod.old_price
                prod.has_discount = (prod.old_price is not None and prod.old_price > prod.price)
                prod.best_option_shop_name = "Amazon"
                prod.best_option_merchant_name = "Amazon"
                prod.best_option_merchant_value = 0
                prod.best_option_shop_logo = static("images/amazon.png")
                prod.best_option_prime_logo = static("images/prime.png")
                prod.best_option_prime = prod.prime
                prod.best_option_url = 'https://www.amazon.es/dp/%s/?tag=thebest511-21' % prod.asin
                #prod.best_option_shipping_cost = prod.shipping_cost
                #prod.best_option_shipping_time = prod.shipping_time
                # Make a list with purchase options (affiliation networks)
                if prod.productpurchaseoption_set.all().count() > 0:
                    options_list = list(prod.productpurchaseoption_set.all())
                else:
                    options_list = list()

                opiniones = []
                opinions = prod.opinion_set.all()
                media_rating=0
                cont=0
                for op in opinions:
                    if op.valid == True:
                        cont+=1
                        media_rating += float(op.rating)
                        opiniones.append(op)
                
                if len(opiniones) > 0:
                    prod.rating = media_rating / int(cont)
                    hay_opiniones = True
                else:
                    prod.rating = 0

                prod.rating = str(prod.rating)
                prod.rating=prod.rating.replace(",",".")
                prod.opiniones = opiniones

                if len(prod.price_list) > 0:
                    try:
                        pricelist = prod.price_list
                        pricetimes = convertlist(pricelist)
                        prod.pricetimes = pricetimes
                    except Exception as e:
                        print(e)
                        pricetimes = []
                        prod.pricetimes = []
                else:
                     prod.pricetimes = []

                hoy = date_today()
                fechahoy = format_date(hoy) # fecha de hoy
                context['fechahoy'] = fechahoy
                month = monthago()
                month_limit = format_date(month) #fecha del intervalo de hace un mes
                context['limite_1mes'] = month_limit
                if len(prod.price_list) > 90:
                    threemonths = threeago()
                    threemonths_limit = format_date(threemonths) #fecha del intervalo de 3 meses
                    context['limite_3meses'] = threemonths_limit
                if len(prod.price_list) > (365/2):
                    sixmonths = sixago()
                    sixmonths_limit = format_date(sixmonths) #fecha del intervalo de seis meses
                    context['limite_6meses'] = sixmonths_limit

                # Set attributes to amazon product and add it to the list
                prod.shop_logo = static("images/amazon.png")
                prod.currency = prod.best_option_currency
                prod.purchase_url = 'https://www.amazon.es/dp/%s/?tag=thebest511-21' % prod.asin
                options_list.append(prod)
                options_list.sort(key=lambda x: x.price)
                prod.other_shops_num = len(options_list) - 1
                if len(options_list) > 0: # Check if price is better than in amazon
                    best_alternative = min(options_list, key=operator.attrgetter('price'))
                    if best_alternative.price < prod.price:
                        # Take price, shop name and attributes from third party alternative
                        prod.best_option_price = best_alternative.price
                        prod.best_option_currency = best_alternative.currency
                        prod.best_option_old_price = best_alternative.old_price
                        prod.has_discount = (best_alternative.old_price is not None and best_alternative.old_price > best_alternative.price)
                        prod.best_option_shop_name = best_alternative.shop_name
                        if 'https' in best_alternative.shop_logo:
                            prod.best_option_shop_logo = best_alternative.shop_logo    
                        else:
                            prod.best_option_shop_logo = best_alternative.shop_logo.replace('http','https')
                        prod.best_option_prime = best_alternative.is_premium
                        prod.best_option_url = best_alternative.purchase_url
                        prod.best_option_shipping_cost = best_alternative.shipping_cost
                        prod.best_option_shipping_time = best_alternative.shipping_time
                        prod.best_option_merchant_name = best_alternative.merchant_name
                        prod.best_option_merchant_value = best_alternative.merchant_value
                        # Remove best option cause is shown appart
                        options_list.remove(best_alternative)
                    else:
                        options_list.remove(prod)

                prod.alternatives = options_list
                for p in options_list:
                    if 'https' in p.shop_logo:
                        p.shop_logo = p.shop_logo
                    else:
                        p.shop_logo.replace('http','https')    

             # Now order by prices
            best15_price_ordered_products = sorted(best15_products, key=lambda x: x.best_option_price)
            best15_price_new_order = sorted(best15_products, key=lambda x: float(x.relevance))

            try:
                if view_mode == 'price1':
                    # Get first group of 5
                    selected_5_ordered_products = best15_price_ordered_products[0:5]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')
                    # Order now by rank
                    selected_5_ordered_products = sorted(selected_5_ordered_products, key=lambda x: float(x.relevance))
                    robots = 'noindex, follow'
                elif view_mode == 'price2':
                    # Get middle group of 5
                    selected_5_ordered_products = best15_price_ordered_products[5:10]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')
                    # Order now by rank
                    selected_5_ordered_products = sorted(selected_5_ordered_products, key=lambda x: float(x.relevance))
                    robots = 'noindex, follow'
                elif view_mode == 'price3':
                    # Get last group of 5
                    selected_5_ordered_products = best15_price_ordered_products[10:15]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')                    
                        # Order now by rank
                    selected_5_ordered_products = sorted(selected_5_ordered_products, key=lambda x: float(x.relevance))
                    robots = 'noindex, follow'
                else: # Best 5 by default
                    selected_5_ordered_products = best15_price_new_order[0:5]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')
                    robots = 'index, follow'
            except Exception as e: # Some error like not having 15 products
                # Then use best 5 by default
                best15_products = context['object'].best5_links.all() # We take 15 products now to be able to group by price
                best15_ranked_products = sorted(best15_products, key=lambda x: x.relevance, reverse=True)
                selected_5_ordered_products = best15_ranked_products[0:5]
                context['has_grouped_prices'] = False
            else:
                group1_prices = [x.best_option_price for x in best15_price_ordered_products[0:5]]
                group2_prices = [x.best_option_price for x in best15_price_ordered_products[5:10]]
                group3_prices = [x.best_option_price for x in best15_price_ordered_products[10:15]]

                if len(group1_prices) == 5 and len(group2_prices) == 5 and len(group3_prices) == 5:
                    context['has_grouped_prices'] = True
                    context['price1_min'] = round_next_down(min(group1_prices))
                    if context['price1_min'] == 0:  # Correction when all prizes are below 10
                        context['price1_min'] = 1
                    context['price1_max'] = round_next_up(max(group1_prices))
                    if context['price1_max'] == 0:  # Correction when all prizes are below 10
                        context['price1_max'] = 10
                    context['price2_min'] = round_next_down(min(group2_prices))
                    if context['price2_min'] < context['price1_max']:
                        context['price2_min'] = context['price1_max']
                    context['price2_max'] = round_next_up(max(group2_prices))
                    context['price3_min'] = round_next_down(min(group3_prices))
                    if context['price3_min'] < context['price2_max']:
                        context['price3_min'] = context['price2_max']
                    context['price3_max'] = round_next_up(max(group3_prices))
                else:
                    context['has_grouped_prices'] = False

            # In mobile view the first product shown is the best one
            context['products_mobile'] = selected_5_ordered_products
            # Change order for web view, where the best product is the third option
            ui_ordered_products = list()
            ui_ordered_products.append(selected_5_ordered_products[0])
            ui_ordered_products.append(selected_5_ordered_products[1])
            ui_ordered_products.append(selected_5_ordered_products[2])
            ui_ordered_products.append(selected_5_ordered_products[3])
            ui_ordered_products.append(selected_5_ordered_products[4])
            context['products'] = ui_ordered_products

            context['hay_opiniones'] = hay_opiniones
            context['pmax'] = pmax

            #Set product category info
            context['active_category'] = active_category
            context['active_category_slug'] = 'https://' + self.request.get_host() + '/categoria/' + active_category_slug + '/'
            #Set page canonical url
            canonical = 'https://' + self.request.get_host() + self.request.path
            context['canonical'] = canonical
            #Set Robots tag content
            context['robots'] = robots
            #Set categories for the top menu
            context['category_images'] = CategoryImage.objects.all().order_by('name')
            context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()

            current_anno = datetime.datetime.now().strftime('%Y')
            context['current_anno'] = current_anno
            current_month_text = datetime.datetime.now().strftime('%B')
            #current_month_text.replace("is", "was")
            context['current_month_text'] = current_month_text

            return context

        else:

            raise Http404


class SearchTagDetailFemale(DetailView):
    queryset = SearchTag.active_objects.all()
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(SearchTagDetailFemale, self).get_context_data(**kwargs)
        active_category=''
        context['is_home'] = False
        context['lazyjs'] = False
        context['valoracionesjs'] = True
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = False

        if context['searchtag'].is_valid:

            search_tag = context['searchtag']
            #category info
            active_category = context['searchtag'].category
            active_category_slug = context['searchtag'].category_slug

            related_links = []
            for related_link in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True).filter(female=True):
                related_links.append(related_link)

            random.shuffle(related_links)    
            context['related_links'] = related_links

            # Trim self path
            if len(search_tag.path.split(' > ')) > 0:
                base_path = ' > '.join(search_tag.path.split(' > ')[:-1])

            # Add related tags
            related_tags = []
            nodes = search_tag.related_tags
            if nodes:
                for i in nodes:
                    tags = SearchTag.objects.filter(browsenode=i)  
                    for tag in tags:
                        related_tags.append(tag)
            else:            
                for related_tag in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True).exclude(id=search_tag.id)[:50]:
                    related_tags.append(related_tag)

            random.shuffle(related_tags)  
            context['related_tags'] = related_tags

            # Add search counter
            SearchTagCounter(tag=search_tag.id).save()

            #Post Info
            article_slug = str(context['searchtag'].slug)
            article_info = Article.objects.filter(slug =search_tag.id).filter(is_ready=True).first()
            context['article_info'] = article_info

            # Get view mode: best / price1 / price2 / price3
            view_mode = self.request.GET.get('view', 'best') # Best 5 by default
            # get best price index
            best5 = context['object']
            #best5 = [x.price for x in best5.best5_links.all()]
            #context['low_price_index'] = best5.index(0.01)

            # Get 15 products ordered by ranking, best one first
            best15_products = context['object'].best5_links.all()[:15] # We take 15 products now to be able to group by price
            best15_ranked_products = sorted(best15_products, key=lambda x: x.rank, reverse=True)

            # Get max and min to normalize ranks
            ranks = [p.rank for p in best15_ranked_products if p.rank > 0] 
            rank_min = 0.01
            #rank_min = float(min(ranks))
            rank_avg = float(sum(ranks)) / max(len(ranks), 1)
            # Adjust offset to show always a value greater than 8
            rank_offset = 8.0
            hay_opiniones = False
            # Select best purchase option / shop based in price
            for prod in best15_ranked_products:
                # Check if recomendations are zero, then set a value between 0.8 and 1.0
                if prod.recommend_percentage == 0:
                   prod.recommend_percentage = 0.8 + (float(random.randrange(1, 19, 1)) / float(100.0))
                # Set best product attributes
                scaled_rank = 0
                try:  # Scale
                    scaled_rank = float(prod.rank) / float(rank_avg)
                    normalized_rank = round((scaled_rank * 0.7) + float(rank_offset), 1)
                except Exception as e:  # Handle errors
                    normalized_rank = rank_offset
                # Normalize and add offset to be between 8.0 and 9.9
                if normalized_rank >= 10.0: # check just in case
                    normalized_rank = 9.9
                normalized_rank_percentaje = int(round(normalized_rank * 10.0, 0))
                
                prod.best_option_rank = "{0:.1f}".format(prod.rank)
                if prod.best_option_rank == '10.0':
                    prod.best_option_rank = '10'
                prod.best_option_rank_percentaje = normalized_rank_percentaje
                prod.best_option_price = prod.price
                prod.best_option_currency = 'EUR'
                prod.best_option_old_price = prod.old_price
                prod.has_discount = (prod.old_price is not None and prod.old_price > prod.price)
                prod.best_option_shop_name = "Amazon"
                prod.best_option_merchant_name = "Amazon"
                prod.best_option_merchant_value = 0
                prod.best_option_shop_logo = static("images/amazon.png")
                prod.best_option_prime_logo = static("images/prime.png")
                prod.best_option_prime = prod.prime
                prod.best_option_url = 'https://www.amazon.es/dp/%s/?tag=thebest511-21' % prod.asin
                #prod.best_option_shipping_cost = prod.shipping_cost
                #prod.best_option_shipping_time = prod.shipping_time
                # Make a list with purchase options (affiliation networks)
                if prod.productpurchaseoption_set.all().count() > 0:
                    options_list = list(prod.productpurchaseoption_set.all())
                else:
                    options_list = list()

                opiniones = []
                opinions = prod.opinion_set.all()
                media_rating=0
                cont=0
                for op in opinions:
                    if op.valid == True:
                        cont+=1
                        media_rating += float(op.rating)
                        opiniones.append(op)
                
                if len(opiniones) > 0:
                    prod.rating = media_rating / int(cont)
                    hay_opiniones = True
                else:
                    prod.rating = 0

                prod.rating = str(prod.rating)
                prod.rating=prod.rating.replace(",",".")
                prod.opiniones = opiniones

                if len(prod.price_list) > 0:
                    try:
                        pricelist = prod.price_list
                        pricetimes = convertlist(pricelist)
                        prod.pricetimes = pricetimes
                    except Exception as e:
                        print(e)
                        pricetimes = []
                        prod.pricetimes = []
                else:
                     prod.pricetimes = []

                hoy = date_today()
                fechahoy = format_date(hoy) # fecha de hoy
                context['fechahoy'] = fechahoy
                month = monthago()
                month_limit = format_date(month) #fecha del intervalo de hace un mes
                context['limite_1mes'] = month_limit
                if len(prod.price_list) > 90:
                    threemonths = threeago()
                    threemonths_limit = format_date(threemonths) #fecha del intervalo de 3 meses
                    context['limite_3meses'] = threemonths_limit
                if len(prod.price_list) > (365/2):
                    sixmonths = sixago()
                    sixmonths_limit = format_date(sixmonths) #fecha del intervalo de seis meses
                    context['limite_6meses'] = sixmonths_limit

                # Set attributes to amazon product and add it to the list
                prod.shop_logo = static("images/amazon.png")
                prod.currency = prod.best_option_currency
                prod.purchase_url = 'https://www.amazon.es/dp/%s/?tag=thebest511-21' % prod.asin
                options_list.append(prod)
                options_list.sort(key=lambda x: x.price)
                prod.other_shops_num = len(options_list) - 1
                if len(options_list) > 0: # Check if price is better than in amazon
                    best_alternative = min(options_list, key=operator.attrgetter('price'))
                    if best_alternative.price < prod.price:
                        # Take price, shop name and attributes from third party alternative
                        prod.best_option_price = best_alternative.price
                        prod.best_option_currency = best_alternative.currency
                        prod.best_option_old_price = best_alternative.old_price
                        prod.has_discount = (best_alternative.old_price is not None and best_alternative.old_price > best_alternative.price)
                        prod.best_option_shop_name = best_alternative.shop_name
                        if 'https' in best_alternative.shop_logo:
                            prod.best_option_shop_logo = best_alternative.shop_logo 
                        else:
                            prod.best_option_shop_logo = best_alternative.shop_logo.replace('http','https')
                        prod.best_option_prime = best_alternative.is_premium
                        prod.best_option_url = best_alternative.purchase_url
                        prod.best_option_shipping_cost = best_alternative.shipping_cost
                        prod.best_option_shipping_time = best_alternative.shipping_time
                        prod.best_option_merchant_name = best_alternative.merchant_name
                        prod.best_option_merchant_value = best_alternative.merchant_value
                        # Remove best option cause is shown appart
                        options_list.remove(best_alternative)
                    else:
                        options_list.remove(prod)

                prod.alternatives = options_list
                for p in options_list:
                    if 'https' in p.shop_logo:
                        p.shop_logo = p.shop_logo
                    else:
                        p.shop_logo.replace('http','https')    

           # Now order by prices
            best15_price_ordered_products = sorted(best15_products, key=lambda x: x.best_option_price)
            best15_price_new_order = sorted(best15_products, key=lambda x: float(x.relevance))

            try:
                if view_mode == 'price1':
                    # Get first group of 5
                    selected_5_ordered_products = best15_price_ordered_products[0:5]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')  
                    # Order now by rank
                    selected_5_ordered_products = sorted(selected_5_ordered_products, key=lambda x: float(x.relevance))
                    robots = 'noindex, follow'
                elif view_mode == 'price2':
                    # Get middle group of 5
                    selected_5_ordered_products = best15_price_ordered_products[5:10]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')
                    # Order now by rank
                    selected_5_ordered_products = sorted(selected_5_ordered_products, key=lambda x: float(x.relevance))
                    robots = 'noindex, follow'
                elif view_mode == 'price3':
                    # Get last group of 5
                    selected_5_ordered_products = best15_price_ordered_products[10:15]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')                   
                    # Order now by rank
                    selected_5_ordered_products = sorted(selected_5_ordered_products, key=lambda x: float(x.relevance))
                    robots = 'noindex, follow'
                else: # Best 5 by default
                    selected_5_ordered_products = best15_price_new_order[0:5]
                    precios = []
                    for p in selected_5_ordered_products:
                        precios.append(p.price)
                        if p.old_price:
                            precios.append(p.old_price)
                        pmax = str(max(precios)).replace(',','.')
                    robots = 'index, follow'
            except Exception as e: # Some error like not having 15 products
                # Then use best 5 by default
                best15_products = context['object'].best5_links.all() # We take 15 products now to be able to group by price
                best15_ranked_products = sorted(best15_products, key=lambda x: x.relevance, reverse=True)
                selected_5_ordered_products = best15_ranked_products[0:5]
                context['has_grouped_prices'] = False
            else:
                group1_prices = [x.best_option_price for x in best15_price_ordered_products[0:5]]
                group2_prices = [x.best_option_price for x in best15_price_ordered_products[5:10]]
                group3_prices = [x.best_option_price for x in best15_price_ordered_products[10:15]]

                if len(group1_prices) == 5 and len(group2_prices) == 5 and len(group3_prices) == 5:
                    context['has_grouped_prices'] = True
                    context['price1_min'] = round_next_down(min(group1_prices))
                    if context['price1_min'] == 0:  # Correction when all prizes are below 10
                        context['price1_min'] = 1
                    context['price1_max'] = round_next_up(max(group1_prices))
                    if context['price1_max'] == 0:  # Correction when all prizes are below 10
                        context['price1_max'] = 10
                    context['price2_min'] = round_next_down(min(group2_prices))
                    if context['price2_min'] < context['price1_max']:
                        context['price2_min'] = context['price1_max']
                    context['price2_max'] = round_next_up(max(group2_prices))
                    context['price3_min'] = round_next_down(min(group3_prices))
                    if context['price3_min'] < context['price2_max']:
                        context['price3_min'] = context['price2_max']
                    context['price3_max'] = round_next_up(max(group3_prices))
                else:
                    context['has_grouped_prices'] = False

            # In mobile view the first product shown is the best one
            context['products_mobile'] = selected_5_ordered_products
            # Change order for web view, where the best product is the third option
            ui_ordered_products = list()
            ui_ordered_products.append(selected_5_ordered_products[0])
            ui_ordered_products.append(selected_5_ordered_products[1])
            ui_ordered_products.append(selected_5_ordered_products[2])
            ui_ordered_products.append(selected_5_ordered_products[3])
            ui_ordered_products.append(selected_5_ordered_products[4])
            context['products'] = ui_ordered_products

            context['hay_opiniones'] = hay_opiniones
            context['pmax'] = pmax

            #Set product category info
            context['active_category'] = active_category
            context['active_category_slug'] = 'https://' + self.request.get_host() + '/categoria/' + active_category_slug + '/'
            #Set page canonical url
            canonical = 'https://' + self.request.get_host() + self.request.path
            context['canonical'] = canonical
            #Set Robots tag content
            context['robots'] = robots
            #Set categories for the top menu
            context['category_images'] = CategoryImage.objects.all().order_by('name')
            context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()

            current_anno = datetime.datetime.now().strftime('%Y')
            context['current_anno'] = current_anno
            current_month_text = datetime.datetime.now().strftime('%B')
            #current_month_text.replace("is", "was")
            context['current_month_text'] = current_month_text

            return context

        else:

            raise Http404


class SearchTagCategoriesList(View):

    def get(self, request, *args, **kwargs):
        context={}
        current_anno = datetime.datetime.now().strftime('%Y')
        context['current_anno'] = current_anno
        current_month_text = datetime.datetime.now().strftime('%B')
        context['current_month_text'] = current_month_text

        context['category_images'] = CategoryImage.objects.all().order_by('name')
        context['categories'] = SearchTag.active_objects.filter(is_valid=True).exclude(category='').exclude(category='Aplicaciones móviles').exclude(category='Hogar').order_by().values('category').distinct()
        context['is_home'] = False
        context['lazyjs'] = True
        context['valoracionesjs'] = False
        context['valoracionesTiendajs'] = False
        context['normal_footer_cat'] = True

        return render(request,'categories.html', context)


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


class RegalosEllosView(AjaxListView):

    context_object_name = "tag_list"
    template_name = "tag_list.html"
    page_template = 'tag_list_page.html'

    def get_queryset(self):
        #slug = self.kwargs.get('slug')
        return SearchTag.active_objects.filter(is_valid=True).filter(for_him=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tag = 'Regalos para Ellos'
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

        for related_link in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True).filter(for_him=True):
            related_links.append(related_link)
        data['related_links'] = related_links

        return data


class RegalosEllasView(AjaxListView):

    context_object_name = "tag_list"
    template_name = "tag_list.html"
    page_template = 'tag_list_page.html'

    def get_queryset(self):
        #slug = self.kwargs.get('slug')
        return SearchTag.active_objects.filter(is_valid=True).filter(for_her=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tag = 'Regalos para Ellas'
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

        for related_link in SearchTag.active_objects.filter(category_slug=active_category_slug).filter(is_valid=True).filter(for_her=True):
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


def opinion(request):
    if request.method == 'POST':
        prodIdTemplate = request.POST['ProdId']
        prodId = prodIdTemplate.replace('.','')
        product_qs = RatedProduct.objects.get(id=prodId)
        product = product_qs
        
        title = request.POST['title']
        name = request.POST['name']
        email = request.POST['email_opinion']
        opinion = request.POST['opinion']
        rating = request.POST['rating']

        if(email != 'admin@thebest5.es'):
            email_qs = Opinion.objects.filter(email=email, product=product)
            if email_qs.exists() or len(email)==0:
                data = {"status" : "404"}
                return JsonResponse(data)
            else:
                Opinion.objects.create(product=product,title=title, opinion=opinion,rating=rating,name=name,email=email)
        else:
            Opinion.objects.create(product=product,title=title, opinion=opinion,rating=rating,name=name,email=email)
    send_mail('The Best 5 :: Nueva Valoración de Producto', 'Un usuario ha dejado una nueva valoración en la web.', 'admin@thebest5.es', ['admin@thebest5.es'])
    return HttpResponse("/")
    

def shopopinion(request):
    if request.method == 'POST':
        shopId = request.POST['ShopId']
        shop_qs = Shop.objects.get(id=shopId)
        shop = shop_qs
        
        title = request.POST['shop_title']
        name = request.POST['shop_name']
        email = request.POST['shop_email_opinion']
        opinion = request.POST['shop_opinion']
        rating = request.POST['shop_rating']

        if(email != 'admin@thebest5.es'):
            email_qs = OpinionShop.objects.filter(email=email, rated_shop=shop)
            if email_qs.exists() or len(email)==0:
                data = {"status" : "404"}
                return JsonResponse(data)
            else:
                OpinionShop.objects.create(rated_shop=shop,title=title,comentario=opinion,rating=rating,name=name,email=email)
                Subscribe.objects.create(email_id=email)
        else:
            OpinionShop.objects.create(rated_shop=shop,title=title,comentario=opinion,rating=rating,name=name,email=email)
    send_mail('The Best 5 :: Nueva Valoración de Tienda', 'Un usuario ha dejado una nueva valoración en la web.', 'admin@thebest5.es', ['admin@thebest5.es'])
    return HttpResponse("/")

def alerts(request):
    if request.method == 'POST':
        prodIdTemplate = request.POST['ProdId']
        prodId = prodIdTemplate.replace('.','')
        product_qs = RatedProduct.objects.get(id=prodId)
        product = product_qs
        tag = SearchTag.objects.filter(best5_links__id=product.id)
        categoria = tag[0].category
        price = request.POST['price_alert']
        email = request.POST['email_alert']
        suscriber = Subscribe.objects.filter(email_id=email)
        d = str(prodId) + ':' + str(price)
        if len(suscriber) == 0:
            Subscribe.objects.create(email_id=email)
            suscriptor = Subscribe.objects.get(email_id=email)
            suscriptor.products.append(d)
            suscriptor.categories.append(categoria)
            suscriptor.save()
        else:
            suscriber[0].products.append(d) 
            suscriber[0].categories.append(categoria)
            suscriber[0].save()
        
    send_mail('The Best 5 :: Nueva Petición de Alerta de Precio', 'Un usuario ha enviado una alerta de precio.', 'admin@thebest5.es', ['admin@thebest5.es'])
    return HttpResponse("/")


def registro(request):
    if request.method == 'POST':
        company = request.POST.get('empresa')
        email = request.POST.get('email_empresa')
        phone = request.POST.get('telefono_empresa')
        message = request.POST.get('message')
        
        body = render_to_string(
            'email_content.html', {
                'name': company,
                'email': email,
                'teléfono': phone,
                'message': message,
            },
        )

        if company and message and email:
            try:
                send_mail('The Best 5 :: Formulario Registro Tienda', body, 'admin@thebest5.es', ['admin@thebest5.es'])
                send_mail('The Best 5', 'Hola! hemos recibido tu petición de registro de tienda. Te responderemos lo antes posible. ¡Muchas gracias! The Best 5 team', 'admin@thebest5.es', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/peticion-enviada/')
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
        return render(request, 'registrar_tienda.html', context)



class RegistroTiendaView(View):

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
        return render(request, 'registrar_tienda.html', context)
    
class TradeDoublerVerificationView(TemplateView):
    template_name = '2983703.html'


class AjaxTagProductsView(IsAdminUser, ChainedSelectChoicesView):
    def get_child_set(self):
        # Return the best 5 products related to the search tag
        products = RatedProduct.objects.filter(searchtag__id=self.parent_value, active=True).order_by('-title')
        return products
    

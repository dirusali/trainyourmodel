from django.conf.urls import include, url
from django.views.generic import TemplateView
#nuevo para redirecciones de url
from django.views.generic.base import RedirectView
from portal import views as portal_views

app_name = 'portal'
from .views import HomeView, upload_csv, FuncionaView, ContactoView, CondicionesView, PrivacidadView, subscribe, successView, contacto


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),  
        url(r'^how-it-works/$', FuncionaView.as_view(), name='funciona'),
        url(r'^subscribe/', subscribe, name="subscribe"),
        url(r'^contact/$', ContactoView.as_view(), name='contacto'),
        url(r'^results/$', results, name='results'),
]


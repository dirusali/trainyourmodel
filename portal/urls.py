from django.conf.urls import include, url
from django.views.generic import TemplateView
#nuevo para redirecciones de url
from django.views.generic.base import RedirectView
from portal import views as portal_views

app_name = 'portal'
from .views import HomeView, upload_csv, FuncionaView, contacto, ContactoView, neural, NeuralView, CondicionesView, PrivacidadView, subscribe, successView, contacto


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),  
        url(r'^how-it-works/$', FuncionaView.as_view(), name='funciona'),
        url(r'^subscribe/', subscribe, name="subscribe"),
        url(r'^contact/', contacto, name='contacto'),
        url(r'^contact/$', ContactoView.as_view(), name='contacto'),
        url(r'^results/$', upload_csv, name='upload_csv'),
        url(r'^deep-learning/$', NeuralView.as_view(), name='neuralview'),
        url(r'^neural-results/$', neural, name= 'neural'),
]


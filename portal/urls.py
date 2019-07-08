
from django.views.generic import TemplateView
#nuevo para redirecciones de url
from django.views.generic.base import RedirectView
from portal import views as portal_views

app_name = 'portal'

from .views import HomeView, FuncionaView, ContactoView, FaqView, TiendasView, RegistroTiendaView, TiendasDetail, CondicionesView, PrivacidadView, SearchTagApi, SearchTagDetail, SearchTagDetailFemale, SearchTagCategoriesList, SearchTagCategoriesDetail, \
    SearchTagView, subscribe, alerts, opinion, shopopinion, TradeDoublerVerificationView, AjaxTagProductsView, registro, successRegistroTiendaView, successView, RegalosEllosView, RegalosEllasView, contacto


urlpatterns = [
    url(r'^/$', HomeView.as_view(), name='home'),
    url('/error404/$', portal_views.error404, name='error404'),
    url('/error500/$', portal_views.error500, name='error500'),
        url(r'^/clustering/$', Clustering.as_view(), name='categories'),
        url(r'^/classification/$', Classification.as_view(), name='categories-detail'),
        url(r'^/categorical/$', 
        url(r'^/supervised/$    
        url(r'^/search/$', SearchTagView.as_view(), name='search'),
        url(r'^/query/$', SearchTagApi.as_view(), name='query'),
        url(r'^/terms-and-conditions/$', CondicionesView.as_view(), name='terms'),
        url(r'^/privacy/$', PrivacidadView.as_view(), name='priv'),
        url(r'^/how-it-works/$', FuncionaView.as_view(), name='funciona'),
        url(r'^/subscribe/', subscribe, name="subscribe"),
        url(r'^/contact/$', ContactoView.as_view(), name='contacto'),
        url(r'^/about/$', RedirectView.as_view(url='/como-funciona/', permanent=True)),
]


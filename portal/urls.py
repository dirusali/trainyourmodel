
from django.views.generic import TemplateView
#nuevo para redirecciones de url
from django.views.generic.base import RedirectView
from portal import views as portal_views

app_name = 'portal'

from .views import HomeView, FuncionaView, ContactoView, FaqView, TiendasView, RegistroTiendaView, TiendasDetail, CondicionesView, PrivacidadView, SearchTagApi, SearchTagDetail, SearchTagDetailFemale, SearchTagCategoriesList, SearchTagCategoriesDetail, \
    SearchTagView, subscribe, alerts, opinion, shopopinion, TradeDoublerVerificationView, AjaxTagProductsView, registro, successRegistroTiendaView, successView, RegalosEllosView, RegalosEllasView, contacto


urlpatterns = [
    url(r'^uk/$', HomeView.as_view(), name='home'),
    url('uk/error404/$', portal_views.error404, name='error404'),
    url('uk/error500/$', portal_views.error500, name='error500'),
    url('uk/message-sent/', successView, name='success'),
    url(r'^uk/gifts-for-men/$', RegalosEllosView.as_view(), name='regalos-ellos'),
    url(r'^uk/gifts-for-women/$', RegalosEllasView.as_view(), name='regalos-ellas'),
    url(r'^uk/petition-sent/$', successRegistroTiendaView, name='registro-tienda'),
        url(r'^uk/categories/$', SearchTagCategoriesList.as_view(), name='categories'),
        url(r'^uk/category/(?P<slug>[-\w]+)/$', SearchTagCategoriesDetail.as_view(), name='categories-detail'),
        url(r'^uk/search/$', SearchTagView.as_view(), name='search'),
        url(r'^uk/query/$', SearchTagApi.as_view(), name='query'),
        url(r'^uk/terms-and-conditions/$', CondicionesView.as_view(), name='terms'),
        url(r'^uk/privacy/$', PrivacidadView.as_view(), name='priv'),
        url(r'^uk/faq/$', FaqView.as_view(), name='faq'),
        url(r'^uk/how-it-works/$', FuncionaView.as_view(), name='funciona'),
        url(r'^uk/best-(?P<slug>[-\w]+|)/$', SearchTagDetail.as_view(), name='detail'),
        url(r'^uk/best(?P<slug>[-\w]+|)/$', SearchTagDetailFemale.as_view(), name='detail-female'),
        url(r'^uk/subscribe/', subscribe, name="subscribe"),
        url(r'^uk/contact/', contacto, name="contacto"),
        url(r'^uk/register-shop/$', RegistroTiendaView.as_view(), name='registrar-tienda'),
        url(r'^uk/contact/$', ContactoView.as_view(), name='contacto'),
        url(r'^uk/about/$', RedirectView.as_view(url='/como-funciona/', permanent=True)),
]


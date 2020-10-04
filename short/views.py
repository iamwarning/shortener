from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from .forms import ShortenerForm
from .models import Enlace


# Create your views here.
class CreateShortener(CreateView):
    model = Enlace
    form_class = ShortenerForm
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_links'] = Enlace.links.total_links()
        context['total_redirects'] = Enlace.links.total_redirects()['redirects']
        return context


class LinkPage(DetailView):
    model = Enlace
    template_name = 'link.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['july'] = Enlace.links.fecha(self.kwargs['pk'])
        return context


class LinkRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        try:
            return Enlace.links.decode_enlace(self.kwargs['code'])
        except IndexError:
            print('Decode sin datos')

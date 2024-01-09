from typing import Any
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from .forms import ShorterForm
from .models import Link
from django.http import HttpResponse
from django.template import loader



class LinksAvailables (CreateView):
    model = Link
    form_class = ShorterForm
    template_name =  'links_available.html'

    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context["totalLinks"] = Link.links.totalLinks()
        context["total_redirections"] = Link.links.totalRedirections()["redirections"]
        return context
    
    
class CreaterShorter(CreateView):
    model = Link
    form_class = ShorterForm
    template_name =  'index.html'

    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context["totalLinks"] = Link.links.totalLinks()
        context["total_redirections"] = Link.links.totalRedirections()["redirections"]
        return context
    
class LinkPage(DetailView):
    model = Link
    template_name = "link.html"
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["month"] = Link.links.dates(self.kwargs["pk"])[0]['month']
        return context
    
    
class RedirectLink(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        try:
            return Link.links.decode_link(self.kwargs["code"])
        except IndexError:
            print("Decode without data")
        


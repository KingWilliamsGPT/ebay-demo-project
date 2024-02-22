import pprint

from django.shortcuts import render
from django.views import generic
from django.http import Http404


from .handleapi import Api
api = Api()

class Index(generic.TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        
        response = api.do_find('shoe')
        
        context['ebay_api'] = response
        context['someitems'] = response.items[:5]
        return context


class SearchPage(generic.TemplateView):
    template_name = 'core/search.html'
    
    def get_context_data(self, **kwargs):
        request = self.request
        query_string = request.GET.get('query_string')

        context = super().get_context_data(**kwargs)
        
        response = api.do_find(query_string)
        
        context['ebay_api'] = response
        context['products'] = response.items
        return context




class ProductView(generic.TemplateView):
    template_name = 'core/product_detail.html'
    
    def get_context_data(self, **kwargs):
        request = self.request
        # query_string = request.GET.get('get_product')

        context = super().get_context_data(**kwargs)
        
        context['ebay_api'] = self.ebay_api
        context['product'] = self.ebay_api.reply.Item
        context['prod'] = pprint.pformat(self.ebay_api.dict()['Item'])
        return context
    

    def get(self, request, product_id):
        response = api.do_find_product_by_id(product_id)
        if not response:
            raise Http404('product not found')
        
        self.ebay_api = response
        return super().get(request)
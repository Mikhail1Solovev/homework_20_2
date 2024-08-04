from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Version
from .forms import ProductForm, VersionForm

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_version'] = Version.objects.filter(product=self.object, is_active=True).first()
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'shop/version_form.html'
    success_url = reverse_lazy('product_list')

class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'shop/version_form.html'
    success_url = reverse_lazy('product_list')

class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'shop/version_confirm_delete.html'
    success_url = reverse_lazy('product_list')

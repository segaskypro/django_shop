from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def get_products_by_category(category_id):
    """Сервисная функция: возвращает продукты категории с низкоуровневым кешированием"""
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        # print(f"  Загружаем из БД и сохраняем в кеш: {cache_key}")
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(cache_key, products, 300)  # TTL = 300 секунд (5 минут)
    else:
        # print(f" Берём из кеша: {cache_key}")

    return products


def category_products_view(request, category_id):
    """Представление для отображения продуктов в категории"""
    products = get_products_by_category(category_id)
    return render(request, 'catalog/category_products.html', {'products': products, 'category_id': category_id})


@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:home')

@method_decorator(cache_page(60), name='dispatch')
class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # print(" ЗАПРОС К БАЗЕ ДАННЫХ! ")
        return Product.objects.filter(is_published=True)

@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        # print(" ЗАПРОС К БАЗЕ ДАННЫХ ДЛЯ ПРОДУКТА! ")
        return super().get_object()


def contacts(request):
    message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message_text')
        message = f"Спасибо, {name}! Ваше сообщение отправлено."
        return render(request, 'catalog/contacts.html', {'message': message})
    return render(request, 'catalog/contacts.html')



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверяем: владелец ИЛИ модератор (с правом can_unpublish_product)
        if obj.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied("Вы не можете редактировать этот продукт")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    template_name = 'catalog/product_confirm_delete.html'
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверяем: владелец ИЛИ модератор
        if obj.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied("Вы не можете удалить этот продукт")
        return super().dispatch(request, *args, **kwargs)
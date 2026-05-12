from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product
from django.views.generic import ListView, DetailView, TemplateView

class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
# def home(request):
#     products = Product.objects.all()  # берём все товары из БД
#     return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message_text')

        # Здесь можно добавить отправку письма или сохранение в базу данных
        # Но по заданию просто показываем сообщение об успехе

        message = f"Спасибо, {name}! Ваше сообщение отправлено."

        # Возвращаем шаблон с сообщением
        return render(request, 'catalog/contacts.html', {'message': message})

    return render(request, 'catalog/contacts.html')


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'catalog/product_detail.html', {'product': product})
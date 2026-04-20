from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    return render(request, 'catalog/home.html')


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
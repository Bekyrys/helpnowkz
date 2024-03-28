import json
import datetime
from .models import *
from .models import Customer

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def redirect_to_instagram(request):
    # URL адрес Instagram, на который вы хотите перенаправить пользователя
    instagram_url = 'https://www.instagram.com/'

    # Используем функцию redirect для перенаправления пользователя на Instagram
    return redirect(instagram_url)

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
    
    context = {'items': items,'order':order}  # Добавляем 'items' в контекст
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
    
    context = {'items': items, 'order': order}  
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action:', action)
    print('productID:', productID)

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productID)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):

    if request.method == 'GET':
        # Отправляем данные о продуктах в шаблон
        products = [
            {"name": "Product 1", "quantity": 2},
            {"name": "Product 2", "quantity": 1},
            # Добавьте остальные продукты здесь
        ]
        product_data = json.dumps(products)
        return render(request, 'checkout.html', {'product_data': product_data})

    

    if request.user.is_authenticated:
        
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)


        custom = request.user.customer
        order, created = Order.objects.get_or_create(customer=custom, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            tel_number = data['shipping'].get('tel_number', '')  # Получаем tel_number из запроса или оставляем пустым, если его нет
            ShippingAddreess.objects.create(
                customer=custom,
                order=order,
                tel_number=tel_number,  # Передаем tel_number в объект ShippingAddress
                address=data['shipping']['address'],
                comment=data['shipping']['comment']
            )
        return JsonResponse({'message': 'Order processed successfully'})  # Возвращает JsonResponse

    else:
        return JsonResponse({'message': 'User is not logged in'})  # Возвращает JsonResponse
    




# Почти реализованная авторизация, регистрация
# from .forms import CreateUserForm
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, authenticate, logout
# # from django.contrib.auth.forms import AuthenticationForm
# # from django.contrib import messages
# # from django import forms


# def registerPage(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Учетная запись была успешно создана')
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('login')  # Имя вашего URL-шаблона для магазина
#     context = {'form': form}
#     return render(request, 'store/register.html', context)



# class EmailAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

# def loginPage(request):
#     form = EmailAuthenticationForm()  # Используем новую форму аутентификации
#     if request.method == 'POST':
#         form = EmailAuthenticationForm(request, request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')  # Получаем электронную почту из формы
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=password)  # Используем электронную почту для аутентификации
#             if user is not None:
#                 login(request, user)
#                 return redirect('store')  # Имя вашего URL-шаблона для магазина
#             else:
#                 form.add_error(None, 'Почта или пароль неверны.')  # Добавляем ошибку к форме

#     context = {'form': form}
#     return render(request, 'store/login.html', context)

# def logoutUser(request):
#     logout(request)
#     return redirect('login')

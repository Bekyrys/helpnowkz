from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.decorators import login_required
import datetime
from .models import Customer


# Create your views here.



def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)\

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
    

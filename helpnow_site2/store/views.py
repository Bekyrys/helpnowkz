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

import json

from django.http import JsonResponse

# def processOrder(request):
#     print('Data', request.POST)
#     return JsonResponse('Complete', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # # userFormData = data['userFormData']
    # shippingInfo = data['shippingInfo']

    # # print('userFormData:', userFormData)
    # print('shippingInfo:', shippingInfo)


    if request.user.is_authenticated:
        custom = request.user.customer
        order, created = Order.objects.get_or_create(customer=custom, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddreess.objects.create(
                customer=custom,
                order=order,
                address=data['shipping']['address'],
                comment=data['shipping']['comment']
            )
        return JsonResponse({'message': 'Order processed successfully'})  # Возвращает JsonResponse

    else:
        return JsonResponse({'message': 'User is not logged in'})  # Возвращает JsonResponse
    

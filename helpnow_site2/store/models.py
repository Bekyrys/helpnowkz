from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete= models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    number = models.CharField(max_length=200)

    def __str__ (self):
        return self.name
    
    # class Meta:
    #     verbose_name = 'Клиент'  # Название модели в единственном числе
    #     verbose_name_plural = 'Клиенты'  # Название модели во множественном числе
    
class Product(models.Model):
    name = models.CharField(max_length= 200)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.png'
        return url
    
    # class Meta:
    #     verbose_name = 'Товар'  # Название модели в единственном числе
    #     verbose_name_plural = 'Товары'  # Название модели во множественном числе




class Order(models.Model):
        customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
        date_ordered = models.DateTimeField(auto_now_add=True)
        complete = models.BooleanField(default = False)
        transaction_id = models.CharField(max_length = 100, null = True)

        def __str__(self):
            return str(self.id)
        
        @property
        def get_cart_total(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.get_total for item in orderitems])
            return total
        
        @property
        def get_cart_items(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.quantity for item in orderitems])
            return total
        
        @property
        def shipping(self):
            shipping = False
            orderitems = self.orderitem_set.all()
            for i in orderitems:
                if i.product.digital == False:
                    shipping = True
            return shipping
        
        # class Meta:
        #     verbose_name = 'Заказ'  # Название модели в единственном числе
        #     verbose_name_plural = 'Заказы'  # Название модели во множественном числе
        
        
        
        

        
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL,  null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.product:
            return self.product.name
        else:
            return "No product"
    

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    # class Meta:
    #         verbose_name = 'Товар заказа'  # Название модели в единственном числе
    #         verbose_name_plural = 'Товар заказов'  # Название модели во множественном числе
    
    
    

class ShippingAddreess(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL,  null=True)
    address = models.CharField(max_length = 200, null=True)
    tel_number = models.CharField(max_length = 200, null=False)
    comment = models.CharField(max_length=255, null=True)  # Добавляем поле для комментариев
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    # class Meta:
    #     verbose_name = 'Адрес доставки'  # Название модели в единственном числе
    #     verbose_name_plural = 'Адреса доставки'  # Название модели во множественном числе
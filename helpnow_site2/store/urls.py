from django.urls import path
#from store import views
from . import views
from .views import redirect_to_instagram

urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path('go-to-instagram/', redirect_to_instagram, name='instagram_redirect'),
    #  path('categories/', categories_list),
    # path('categories/<int:category_id>/', category_detail),
    # path('categories/<int:category_id>/subcategories/', subcategories_list),
    # path('products/<int:product_id>/', product_detail),








    # path("register/", views.registerPage, name="register"),
    # path("login/", views.loginPage, name="login"),
    # path("logout/", views.logoutUser, name="logout"),
    

]
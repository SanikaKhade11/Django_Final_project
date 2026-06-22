from django.urls import path
from .views import*

urlpatterns=[
    path('',home,name='home'),
    path('cart/',cart, name='cart'),
    path('addtocart/<int:id>',addtocart,name='addtocart'),
    path('removefromcart/<int:id>',removefromcart,name='removefromcart'),
    path('incrementQty/<int:id>',incrementQty,name='incrementQty'),
    path('decrementQty/<int:id>',decrementQty,name='decrementQty')
]
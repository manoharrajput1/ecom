from django.urls import path
from . import views


urlpatterns = [
    path('index',views.index, name='index'),
    path('',views.signin, name='login'),
    path('cart/',views.cart, name='cart'),
    path('signup/',views.signup, name='signup'),
    path('logout_req/',views.logout_req, name='logoutreq'),
    path('checkout/',views.checkout, name='checkout'),
    # path('prodView/<int:myid>',views.prodView, name='prodView'),
    path('update_item/',views.updateItem, name='update_item'),
    path('viewpred/',views.viewPred, name='viewpred'),
    path('process_order/',views.processOrder, name='processOrder'),
]
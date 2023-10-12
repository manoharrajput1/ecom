from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect, render
from .models import *
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from itertools import chain
import json
import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        products = []
        prodcat = Product.objects.values('subcategory')
        categories = { item['subcategory'] for item in prodcat}
        catlen = range(0,len(categories))
        for cate in categories:
            product = Product.objects.filter(subcategory=cate)
            products.append([product,catlen])
        # print(products)    
        context = {'products': products, 'cartItems': cartItems}
        return render(request, 'index.html', context)
    else:
        return redirect('/')    

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)   

def checkout(request):
    data = cartData(request)
    userdata = request.user
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems,'userdata':userdata}
    return render(request, 'checkout.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email registered')
                return redirect('/signup')   
            else:  
                user = User.objects.create_user(username=username,email=email, password=password)
                user.save()  
                return redirect('/')
    else:
        return render(request, 'signup.html') 
        
       

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/index')
        else:
            messages.info(request, 'invalid details')    
    else:
        return render(request, 'signin.html')

def logout_req(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        user=user)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def cartData(request):
    user = request.user
    order, created = Order.objects.get_or_create(user=user)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    return {'cartItems': cartItems, 'order': order, 'items': items}


def processOrder(request):
    user = request.user
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    order, created = Order.objects.get_or_create(user=user)
    total = float(data['ord']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.save()
    ShippingAddress.objects.create(
        user=user,
        order=order,
        address=data['ship']['address'],
        city=data['ship']['city'],
        state=data['ship']['state'],
        zipcode=data['ship']['zipcode'],
    )
    return JsonResponse('Payment submitted..', safe=False)


def predict(productId):
    products = Product.objects.all().values()
    df = pd.DataFrame(products)
    df2 = df.drop(axis=1, columns=['id', 'name', 'product_image', 'desc','quantity' ])
    scaler = MinMaxScaler()
    x = df2.drop(axis=1, columns=['price'])
    y = pd.get_dummies(x)
    data = df2[['price']]
    scaler.fit(data)
    data = scaler.transform(data)
    y['price'] = data
    # print(y)
    df_list = y.values.tolist()
    # print(df_list)
    datalist = []
    a = df_list[int(productId)-1]
    # print(a)
    for i in df_list:
        # print(i)
        ndata = cosine_similarity([a], [i])
        ndata = ndata.tolist()
        datalist.append(ndata)
    flatten_list = list(chain.from_iterable(datalist))
    newlist = list(chain.from_iterable(flatten_list))
    b = np.array(newlist)
    # print(b)
    idx = (-b).argsort()[1:5]
    # print(idx)
    return idx



def prodView(request, myid):
    productId = myid
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.filter(id=myid)
    idx = predict(productId)
    # print(idx)
    prodl = []
    for i in idx:
        # print(i)
        prod = Product.objects.get(id=i+1)
        prodl.append(prod)
    context = {'product': product, 'cartItems': cartItems, 'prodl':prodl}
    return render(request, 'prodview.html', context)
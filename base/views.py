from django.shortcuts import render,redirect
from .views import*
from .models import Product,Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    print(request.GET)
    if request.user.is_authenticated:
        cartproductCount = Cart.objects.filter(host = request.user).count()
    
    else:
        cartproductCount = 0

    no_match = False
    trend=False
    offer=False
    
    if 'search' in request.GET:
        search = request.GET['search']
        print(search)
        data = Product.objects.filter(Q(pname__icontains = search) | Q(pdesc__icontains = search))
        
        if len(data) == 0:
            no_match = True
            
    elif 'category' in request.GET:
        category = request.GET['category']
        data = Product.objects.filter(pcategory=category)
    
    elif 'trading' in request.GET:
        data = Product.objects.filter(trading=True)
        trend=True
        print(data)
    
    elif 'offer' in request.GET:
        data = Product.objects.filter(offer=True)
        offer=True
    else:
        data = Product.objects.all()

    #category present in Database
    a = Product.objects.all()
    category = []
    for i in a:
        if i.pcategory not in category:
            category+=[i.pcategory]
    print(category)
    return render(request,'home.html' , {'data':data, 'no_match' : no_match, 'category':category, 'search_bar':True, 'trend': trend, 'offer':offer, 'cartproductCount': cartproductCount})

@login_required(login_url = 'login_')
def cart(request):
    cartproducts = Cart.objects.filter(host = request.user)
    # total price 
    total_price = 0

    # count of product
    cartproductCount = 0
    cartproductCount = Cart.objects.filter(host = request.user).count()
    for i in cartproducts:
        total_price+=i.totalprice
        # cartproductCount+=i.quantity
    print(total_price)
    print(cartproductCount)

    return render(request, 'cart.html', {'cartproducts' : cartproducts, 'total_price':total_price, 'cartproductCount': cartproductCount})

@login_required(login_url = 'login_')
def addtocart(request,id):
    product = Product.objects.get(id=id )
    try:
        cp = Cart.objects.get(pname=product.pname, host=request.user)
        cp.quantity += 1
        cp.totalprice += product.price
        cp.save()
    except:
        Cart.objects.create(
        # pimage=product.pimage,
        pname = product.pname,
        price = product.price,
        pcategory=product.pcategory,
        quantity=1,
        totalprice=product.price,
        host=request.user
    )
    return redirect('cart')

@login_required(login_url = 'login_')
def removefromcart(request,id):
    cartproducts = Cart.objects.get(id = id)
    cartproducts.delete()
    return redirect('cart')

@login_required(login_url = 'login_')
def incrementQty(request,id):
    cartproduct=Cart.objects.get(id =id)
    cartproduct.quantity+=1
    cartproduct.totalprice+=cartproduct.price
    cartproduct.save()
    return redirect('cart')

@login_required(login_url = 'login_')
def decrementQty(request,id):
    cartproduct=Cart.objects.get(id = id)

    if cartproduct.quantity>=1:
        cartproduct.quantity-=1
        cartproduct.totalprice-=cartproduct.price
        cartproduct.save()
    else:
        cartproduct.delete()
    
    return redirect('cart')


def support(request):
    return render(request, 'support.html')

def knowUs(request):
    return render(request, 'knowus.html')


from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import ProductForm
from django.contrib import messages
from .models import Product
from django.http import JsonResponse
from .models import *
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
def app(request):
    return render(request,'app.html')

def contact(request):
    return render(request,'contact.html')

def footer(request):
    return render(request,'footer.html')
    

def about(request):
    return render(request,'about.html')

def search(request):
    search_data=request.POST.get('search_data')
    data=Product.objects.filter(name__icontains=search_data)
    context={'data':data}
    return render(request,'search.html',context)

def powertools(request):
    powertools=Product.objects.filter(category='power_tools_and_accessories').all()
    context={'powertools':powertools}
    return render(request,'powertools.html',context)
    

def aircompressor(request):
    aircompressor=Product.objects.filter(category='air compressor').all()
    context={'aircompressor':aircompressor}
    return render(request,'aircompressor.html',context)

def machinetools(request):
    machinetools=Product.objects.filter(category='machine_tools').all()
    context={'machinetools':machinetools}
    return render(request,'machinetools.html',context)
    




def index(request):
    products = Product.objects.all()
    context ={'products':products,}
    return render(request,'index.html',context)

def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message':'Invalid login Credentials'})
    else:
        return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        address=request.POST['address']
        phone=request.POST['phone']
        name=request.POST['name']
        password=request.POST['password']

        user=User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        customer=Customer.objects.create(
            user=user,
            phone=phone,
            address=address,
            name=name
        )
        return redirect(' ')
    return render(request,'signup.html')


def logout_view(request):
    logout(request)
    return redirect('index')

def addproduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        # Create a new Product instance and save it to the database
        Product.objects.create(name=name, price=price, category=category, image=image)
        
        messages.success(request,"Success")
        return redirect('addproduct')
    return render(request,'addprod.html')

def description(request,pk):
    product = get_object_or_404(Product, pk=pk)
    context={'product':product}
    return render(request,'description.html',context)

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

        # Save product_id and quantity in the session
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart

        return redirect('cart')  # Redirect to the cart page
    return redirect('index')


def cart(request):
    # Retrieve the cart dictionary from the session, if it exists, or an empty dictionary if it doesn't.
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0        
    
    # Iterate over each key-value pair in the cart dictionary.
    for product_id, quantity in cart.items():
        # Fetch the corresponding Product object from the database using the product ID.
        product = Product.objects.get(pk=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    context = {'cart_items': cart_items, 'total_price': total_price}
    
    return render(request, 'cart.html', context)




def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # Retrieve the cart from the session
        cart = request.session.get('cart', {})
        
        # Check if the product is in the cart
        if product_id in cart:
            # Remove the product from the cart
            del cart[product_id]
            # Save the updated cart back to the session
            request.session['cart'] = cart
            
    # Redirect back to the cart page or any other page
    return redirect('cart') 

def checkout(request):
    cart = request.session.get('cart', {})
    
    if request.method == 'POST':
        # Process checkout information and clear the cart
        request.session['cart'] = {}
        
        # Redirect to a thank you page or any other page
        return redirect('placeorder')  # Replace 'thank_you' with the URL name of your thank you page
    
    # Fetch products in the cart
    cart_products = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    context = {
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)


def shipping_info(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')

        # Create a new ShippingInfo object and save it to the database
        ShippingInfo.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=address,
            city=city,
            zip_code=zip_code
        )
        return redirect('payment')
        # Initialize Razorpay client with your API key and secret        

    return render(request, 'placeorder.html')

def payment(request):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    cart = request.session.get('cart', {})
    
    # Calculate the total amount from the items in the cart
    total_amount = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        total_amount += product.price * quantity
    
    # Ensure that the total amount is at least INR 1.00
    if total_amount < 1:
        total_amount = 1
    
    # Create a Razorpay order
    order = client.order.create({
        'amount': total_amount * 100,  # Razorpay expects amount in paisa
        'currency': 'INR',
        'payment_capture': 1  # Automatically capture payment when order is created
    })
    
    context = {'order': order}
    return render(request, 'razorpay_payment.html', context)
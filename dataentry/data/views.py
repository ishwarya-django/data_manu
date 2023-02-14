from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,logout,login
from django import forms
from.forms import RegistrationForm,Product_addform,Sell_priceform,Expense_Product_Form,Purchase_Product_Form,Add_Expense_Form
from.models import User,Makeproduct,Expense_Product,Add_Expense
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
 
from twilio.rest import Client



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data.get('confirm_password')

            if password != confirm_password:
                raise forms.ValidationError(
                    "Password does not match!"
                )
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            return redirect('login')
        
           
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'data/register.html', context)


def login(request):
    print
    if request.method == 'POST':
        print("hii")
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)

        user = auth.authenticate(email=email, password=password)
        print(user)
        if user:
            print("hg")
            auth.login(request, user)
            messages.success(request,f"Welcome {user.username}")
            return redirect('add_product')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request,'data/login.html')

# def login(request):
    
#     if request.method=="POST":
        
#         form=AuthenticationForm(request,data=request.POST)
#         if form.is_valid():
#             x=form.cleaned_data.get('email')
#             print(x)
#             y=form.cleaned_data.get('password')
#             print(y)
#             user=authenticate(email=x,password=y)
#             if user:
#                 login(request,user)
                
#                 return redirect('add_product')
#             else:

#                 return redirect('login')
         
#         else:
#             print(form.errors)
#             return render(request,"data/login1.html",{'form':form})
#     else:
#         return render(request,"data/login1.html")
    
@login_required(login_url = 'login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def add_product(request):
    form=Product_addform()
    x=Makeproduct.objects.all()
    if request.method=="POST":
        form=Product_addform(request.POST)
        x=Makeproduct.objects.all()
        product_name=request.POST.get("product_name")
        product=Makeproduct.objects.filter(product_name=product_name)
        for i in product:
            namee=Makeproduct.objects.filter(product_name=i.product_name)
            for j in namee:
                print(j.product_name)
        name=[]
        name.append(product_name)
        msg=[]
        try:
            if product_name == j.product_name:
               msg.append('product name already exists')
                
            else:
                    msg.append(None)
        except:
                msg.append(None)  
        t=zip(name,msg)
        for i in msg:  
          if i is not None:
            return render(request,'data/add_product.html',{'form':form,'t':t,'x':x})  
        if form.is_valid():
            form.save()
            messages.success(request,'product addded successfully')
            return redirect('add_product')
        else:
            return render(request,'data/add_product.html',{'form':form,'x':x})  
         
    return render(request,'data/add_product.html',{'x':x})

def sell_price(request,id):
    product=Makeproduct.objects.get(id=id)
    form=Sell_priceform()
    if request.method=="POST":
        product=Makeproduct.objects.get(id=id)
        form=Sell_priceform(request.POST)
        amt=[]
        msg=[]
        price= request.POST.get('sell_price')
        amt.append(price)
        
        try:
                typ = float(price)
                t=str(typ).split('.')[1]
                if len(t) > 2:
                    msg.append('more than 2 decimal_places')
                
                else:
                    msg.append(None)

        except:
                msg.append('enter a number')
        z=zip(amt,msg)
        for i in msg:
            if i is not None:
                return render(request,'data/sell_price.html',{'z':z,'product':product})   
        sell=request.POST.get('sell_price')
        if form.is_valid():
            product.sell_price=sell
            product.save()
            if float(product.sell_price) > float(product.makeproduct_price):

                product.status_makeproduct="profit"
                profit=float(product.sell_price) - float(product.makeproduct_price)
                product.pro_loss_makeproduct=profit
                product.save()
            elif float(product.sell_price) < float(product.makeproduct_price):
                product.status_makeproduct="loss"
                loss=float(product.makeproduct_price) - float(product.sell_price)
                product.pro_loss_makeproduct=loss
                product.save()
            messages.success(request,'sell_price addded successfully')
            return redirect('add_product')
        
    return render(request,'data/sell_price.html',{'product':product})


def expense(request,id):
    product=Makeproduct.objects.get(id=id)
    y=Expense_Product.objects.filter(org_product=product)
    form=Expense_Product_Form()
    if request.method=="POST":
        product=Makeproduct.objects.get(id=id)
        y=Expense_Product.objects.filter(org_product=product)
        form=Expense_Product_Form(request.POST)
        amt=[]
        msg=[]
        price= request.POST.get('price')
        amt.append(price)
        
        try:
                typ = float(price)
                t=str(typ).split('.')[1]
                if len(t) > 2:
                    msg.append('more than 2 decimal_places')
                
                else:
                    msg.append(None)

        except:
                msg.append('enter a number')
        z=zip(amt,msg)
        for i in msg:
            if i is not None:
                return render(request,'data/expense.html',{'z':z,'product':product,'y':y,'form':form})   
        price=request.POST.get('price')

        if form.is_valid():
            x=form.save()
            x.org_product=product
            x.save()
            makepro_price=0
            for i in y:
              makepro_price+=i.price
            product.makeproduct_price=makepro_price
            product.save()  
            if float(product.sell_price) > float(product.makeproduct_price):
                product.status_makeproduct="profit"
                profit= product.sell_price - product.makeproduct_price
                product.pro_loss_makeproduct=profit
                product.save()
            elif float(product.makeproduct_price) > float(product.sell_price)  :
                product.status_makeproduct="loss"
                loss= product.makeproduct_price - product.sell_price
                product.pro_loss_makeproduct=loss
                product.save()
            messages.success(request,'expense addded successfully')
            return render(request,'data/expense.html',{'product':product,'y':y})   
        else:
            return render(request,'data/expense.html',{'product':product,'y':y,'form':form})
    return render(request,'data/expense.html',{'product':product,'y':y})

def purchasepro(request,id):
    product=Makeproduct.objects.get(id=id)
    form=Purchase_Product_Form()
    if request.method=="POST":
        product=Makeproduct.objects.get(id=id)
        form=Purchase_Product_Form(request.POST)
        amt=[]
        msg=[]
        price= request.POST.get('price_pro_fromshop')
        amt.append(price)
        
        try:
                typ = float(price)
                t=str(typ).split('.')[1]
                if len(t) > 2:
                    msg.append('more than 2 decimal_places')
                
                else:
                    msg.append(None)

        except:
                msg.append('enter a number')
        z=zip(amt,msg)
        for i in msg:
            if i is not None:
                return render(request,'data/purchasepro.html',{'z':z,'product':product})   
        sell=request.POST.get('price_pro_fromshop')
        if form.is_valid():
            product.price_pro_fromshop=sell
            product.save()
            if float(product.price_pro_fromshop) > float(product.makeproduct_price):
                product.status_purchaseproduct="profit"
                profit=float(product.price_pro_fromshop) - float(product.makeproduct_price)
                product.pro_loss_purchaseproduct=profit
                product.save()
            elif float(product.price_pro_fromshop) < float(product.makeproduct_price):
                product.status_purchaseproduct="loss"
                loss=float(product.makeproduct_price) - float(product.price_pro_fromshop)
                product.pro_loss_purchaseproduct=loss
                product.save()
            messages.success(request,'product price addded successfully')
            return redirect('add_product')
        
    return render(request,'data/purchasepro.html',{'product':product})

def layout(request):
     return render(request,'data/layout.html')

def add_expense(request):
    x=Add_Expense.objects.all()
    form=Add_Expense_Form()
    if request.method=="POST":
        x=Add_Expense.objects.all()
        form=Add_Expense_Form(request.POST)
        product=request.POST.get("product")
        product=Add_Expense.objects.filter(product=product)
        for i in product:
            namee=Add_Expense.objects.filter(product=i.product)
            for j in namee:
                print(j.product)
        name=[]
        name.append(product)
        msg=[]
        try:
            if product == j.product:
               msg.append('product name already exists')   
            else:
                    msg.append(None)
        except:
                msg.append(None)  
    
        z=zip(name,msg)
        for i in msg:  
          if i is not None:
            return render(request,'data/add_expense.html',{'form':form,'z':z,'x':x})  
        product=request.POST.get("product")
        if form.is_valid():
            form.save()
            messages.success(request,f"{product} expense details added successfully")
            return render(request,'data/add_expense.html',{'x':x})
        else:
            return render(request,'data/add_expense.html',{'form':form,'x':x})
    return render(request,'data/add_expense.html',{'x':x})

account_sid = 'ACb4eb7c5ab678c75d85c41d87fd7cd71e'
auth_token = 'd3ab13a4f0d0cf6fb62daf641edba343'
client = Client(account_sid, auth_token)


@csrf_exempt
def index(request):
    if request.method=="POST":
        
        message = client.messages.create(
                              from_='whatsapp:+14155238886',
                              body='Hello, there!',
                              to='whatsapp:+8903201360'
                          )
        return HttpResponse("hello")
    return  render(request,'data/what.html')
from django.shortcuts import render,HttpResponse,redirect
from storeapp.models import Product,Cart,Orders
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.

'''
def function_name(request):
    function body
    return HttprResponse(data)
'''

def home(request):
    p=Product.objects.all()
    print(p)
    #return HttpResponse('data fetched')
    #context={}
    #context['User']="itvedant"
    #context['x']=30
    #context['y']=40
    #context['l']=[1,2,3,4,5]
    #context['d']={'id':1,'name':'machine','price':200,'qty':50}
    #context['data']=[
     #   {'id':1,'name':'machine','price':200,'qty':50},
     #   {'id':2,'name':'sunny','price':20,'qty':5},
    #  {'id':3,'name':'jeans','price':100,'qty':2}
    #]
    context={}
    context['products']=p
    return render(request,'home.html',context)


def delete(request,rid):
    p=Product.objects.filter(id=rid)
    p.delete()
    return redirect('/home')

def edit(request,rid):

    if request.method=='GET':
        p=Product.objects.filter(id=rid) # fetching a specific record, sql= select * from storeapp_product where id=id
        context={}
        context['data']=p
        return render(request,'editproduct.html',context)
    else:
        uname=request.POST['pname']
        uprice=request.POST['price']
        uqty=request.POST['qty']
        # print(uname,uprice,uqty)
        # return HttpResponse('updated')
        p=Product.objects.filter(id=rid)
        p.update(name=uname,price=uprice,qty=uqty)
        return redirect('/home')
        
def greet(request):
    return render(request,'base.html')

def addproduct(request):
    print(request.method)
    if request.method=='GET':
        return render(request,'addproduct.html')
    
    else:
        #print('in else part')
        p_name=request.POST['pname']
        price=request.POST['price']
        qty=request.POST['qty']

        #to insert user into database
        p=Product.objects.create(name=p_name,price=price,qty=qty)
        print("Product_object:",p)
        p.save()
        return redirect('/home')

        #function views for ecommerce application

def index(request):
    uid=request.user.id
    print('user id:',uid)
    print(request.user.username)
    print(request.user.is_authenticated)
    p=Product.objects.filter(is_active=True)
    #print(p)
    context={}
    context['product']=p
    return render(request,'index.html',context)        


def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=1)
    #p=Product.objects.filter(cat=cv)
    #print(p)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['product']=p
    return render(request,'index.html',context)

def pricerange(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=1)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['product']=p
    return render(request,'index.html',context)       
    
    
def sort(request,sv):
    if sv == '1':
        para='-price'
    else:
        para='price'

    p=Product.objects.order_by(para).filter(is_active=1)
    context={}
    context['product']=p
    return render(request,'index.html',context)


def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def cart(request):
    return render(request,"cart.html")

def payment(request):
    return render(request,"payment.html")

#def login(request):
    #return render(request,"login.html")

def register(request):
    context={}
    if request.method=="GET":
        return render(request,"register.html")
    else:
        #data fetch 
        user=request.POST['uname']
        email=request.POST['umail']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        #validation
        if user=='' or email=='' or p=='' or cp=='' :
            context['errmsg']="Fields cannot be Empty"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Password and confirm Password dosn't match"
            return render(request,'register.html',context)
        else:
            #insert 
            try:
                # u=User.objects.create(username=user,password=p)
                 u=User.objects.create(username=user)
                 u.set_password(p)
                 u.save()
                 context['success']="User Registration Successfull"
                 return render(request,"register.html",context)
            except Exception:
                context['errmsg']="User Registration Successfull"
                return render(request,"register.html",context)


           
        

def details(request,id):
    p=Product.objects.filter(id=id)
    #print(p)
    context={}
    context['products']=p
    return render(request,'details.html',context)

def user_login(request):
    context={}
    if request.method=='GET':
        return render(request,'login.html')
    else:
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname)
        #print(upass)

        u=authenticate(username=uname,password=upass)
        if u is not None:
            login(request,u)
            return redirect('/index')
        else:
            context['errmsg']="Invalide username or password!!!"
            return render(request,'login.html',context)


def user_logout(request):
    logout(request)
    return redirect("/index") 

def addcart(request,rid):
    
    if request.user.is_authenticated:
        context={}
        p=Product.objects.filter(id=rid)
        u=User.objects.filter(id=request.user.id)
        q1=Q(pid=p[0])
        q2=Q(uid=u[0])
        res=Cart.objects.filter(q1 & q2)
        if res:
            context['dup']="Product Already Added"
            context['products']=p
            return render(request,'details.html',context)
        else:
            u=User.objects.filter(id=request.user.id)
            #print(u)
            #print(u[0])
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['products']=p
            context['success']="Product Added Successfully To Cart"
            return render(request,'details.html',context)

    else:
        return redirect('/login')
    
    return HttpResponse("in cart")

def viewcart(request):
    context={}
    if request.user.is_authenticated:
        print("In if part")
        print(request.user.id)
        c=Cart.objects.filter(uid=request.user.id)
        print(c)
        cp=len(c)
        print("Count:",cp)
        s=0
        for x in c:
            print(x)
            print(x.qty)
            print(x.pid.price)
            s=s+(x.qty*x.pid.price)

        print("summation or total:",s)
        context['total']=s
        context['cdata']=c
        context['items']=cp
        return render(request,'cart.html',context)
    
    else:
        return redirect('/login')

def removecart(request,rid):
    c=Cart.objects.get(id=rid)
    c.delete()
    return redirect('/cart')

def cartqty(request,sig,pid):
    q1=Q(uid=request.user.id)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    #print(c)
    qty=c[0].qty
    if sig=='0':
        if qty>1:
            qty=qty-1
            c.update(qty=qty)
        
    else:
        qty=qty+1
        c.update(qty=qty)

    #print("Existing:",qty)
    return redirect("/cart")

def place_order(request):
    if request.user.is_authenticated:
        context={}
        c=Cart.objects.filter(uid=request.user.id)
        oid=random.randrange(1000,9999)
        print("order Id:",oid)
        s=0
        for x in c:
            o=Orders.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
            o.save()
            x.delete()
        

        o=Orders.objects.filter(uid=request.user.id)
        i=len(o)
        for y in o:
            s=s+(y.qty*y.pid.price)
                                
        context['cdata']=o
        context['total']=s
        context['items']=i
        return render(request,'placeorder.html',context)
    else:
        return redirect('/login')


def payment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_6SRzEueEmotQTa", "RuDfoC6JlKjZl5dHy49DFJGA"))
    #print(client)
    o=Orders.objects.filter(uid=request.user.id)
    #print(o)
    oid=str(o[0].order_id)
    s=0
    for y in o:
        s=s+(y.qty*y.pid.price)
    #print("Order Id:",oid)
    #print("Total:",s)
    s=s*100 # paise to Rs
    data = { "amount":s, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data) 
    print(payment) 
    context['payment']=payment

    return render(request,'payment.html',context)

def sendmail(request):
    pid=request.GET['p1']
    oid=request.GET['p2']
    sign=request.GET['p3']
    rec_emai=request.user.email
    #print(rec_email)
    #print("payment ID:",pid)
    #print("order ID:",oid)
    #print("Signature:",sign)
    msg='Your Order Placed Successfully. Your Order Tracking ID:'+oid
    send_mail(
        "Ekart Order Status",
        msg,
        "atishwarang89@gmail.com",
        [rec_email],
        fail_silently=False,
        )
    return HttpResponse("Email Send")

def mailmsg(request):
    return render(request,'email.html')
       

def entermail(request):
    return render(request,'entermail.html')


def enterotp(request):
    return render(request,'enterotp.html')






    

    




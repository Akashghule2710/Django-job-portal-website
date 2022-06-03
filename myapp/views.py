from django import views
from django.shortcuts import redirect, render
from .models import *
from random import randint

# Create your views here.

def IndexPage(request):
    return render(request,"myapp/index.html")

def SignupPage(request):
    return render(request,"myapp/signup.html")


def RegisterUser(request):
    if request.POST['role'] == "Candidate":
        role= request.POST['role']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user = UserMaster.objects.filter(email=email)
        if user:
            message = "user already exists"
            return render(request,"myapp/signup.html",{'msg':message})
        else:
            if password == cpassword:
                otp = randint(100000,999999)
                newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                usercand = Candidate.objects.create(user_id = newuser,firstname = fname,lastname = lname)
                return render(request,"myapp/otpverify.html",{'email':email})
    else:
        role = request.POST['role']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user1 = UserMaster.objects.filter(email=email)
        if user1 :
            message = "user already exists"
            return render(request,"myapp/signup.html",{'msg':message})
        else:
            if password == cpassword:
                otp = randint(100000,999999)
                newuser1 = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                newcand1 = Company.objects.create(user_id = newuser1,firstname = fname,lastname = lname)
                return render(request,"myapp/otpverify.html",{'email':email}) 

def OtpPage(request):
    return render(request,"myapp/otpverify.html")

def OtpVerify(request):
    email = request.POST['email']
    otp = int(request.POST['otp'])
    user = UserMaster.objects.get(email=email)
    if user:
        if user.otp == otp:
            message = "otp verified succesfully"
            return render(request,"myapp/login.html",{'msg':message})
        else:
            message = "otp incorrect"
            return render(request,"myapp/otpverify.html",{'msg':message})
    else:
        return render(request,"myapp/signup.html")

def Loginpage(request):
    return render(request,"myapp/login.html")

def LoginUser(request):
    if request.POST['role']=="Candidate":
        email = request.POST['email']
        password = request.POST['password']

        user = UserMaster.objects.get(email=email)
        if user:
            if user.password == password and user.role == "Candidate":
                can = Candidate.objects.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = can.firstname
                request.session['lastname'] = can.lastname
                request.session['email'] = user.email
                return redirect('index')
            else:
                message = "password does not exists"
                return render(request,"myapp/login.html",{'msg':message})
        else:
            message = "user does not exists"
            return render(request,"myapp/login.html",{'msg':message})
    else:
        email = request.POST['email']
        password = request.POST['password']

        user2 = UserMaster.objects.get(email=email)
        if user2:
            if user2.password == password and user2.role == "Company":
                cam = Company.objects.get(user_id=user2)
                request.session['id'] = user2.id
                request.session['role'] = user2.role
                request.session['firstname'] = cam.firstname
                request.session['lastname'] = cam.lastname
                request.session['email'] = user2.email
                return redirect('index')
            else:
                message = "password does not exists"
                return render(request,"myapp/login.html",{'msg':message})
        else:
            message = "user does not exists"
            return render(request,"myapp/login.html",{'msg':message})


#profile page view
def ProfilePage(request,pk):
    user = UserMaster.objects.get(pk=pk)
    can = Candidate.objects.get(user_id = user)
    return render(request,"myapp/profile.html",{'user':user,'can':can})  

#update profile view
def UpdateProfile(request,pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Candidate":
        can = Candidate.objects.get(user_id = user)
        can.state = request.POST['state']
        can.city = request.POST['city']
        can.address = request.POST['address']
        can.dob = request.POST['dob']
        can.gender = request.POST['gender']
        can.profile_pic = request.POST['image']
        can.save()
        url = f'/profile/{pk}'
        return redirect(url)





            
        

    



            
                





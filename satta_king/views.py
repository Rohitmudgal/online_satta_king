from http import client
from tokenize import Number
from turtle import title, update
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .models import *
import razorpay
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .helpes import send_forget_password_mail
import uuid

import time



def Login(request):
    if request.method == "POST":
        phonenumber=request.POST.get('username')
        password=request.POST.get('password')
        
        user = auth.authenticate(username=phonenumber,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Invalid Username/Password")
            return redirect("login")
    else:   
        return render(request,'login.html')

def SignUp(request):
    if request.method =='POST':
        name=request.POST.get('first_name')
        phonenumber=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        if password==repassword:
            if User.objects.filter(username=phonenumber ).exists():
                messages.info(request,"Username Already Exists.")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Already Exists.")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=phonenumber,first_name=name,email=email,password=password)
                user.save()
                points=request.POST.get('points')
                userpoint=POINTS(points=points,user=user)
                userpoint.save()
                send_mail(
                    'Account Create',
                    f'Welcome {user.first_name} to Online Satta King.Your Account Has Create Secessfully.Your Joinning Bounus {userpoint.points} Points Credit in Your Account',
                    'onlinesattaking83@gmail.com',
                    [email],
                    fail_silently=False,
                    )
                messages.info(request,"Account Created.")
                return redirect('home')
        else:
            messages.info(request,"password mismatch")
            return redirect('signup')
    return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def ForgetPassword(request):
    if request.method=="POST":
        username=request.POST.get('username')
        
        if not User.objects.filter(username=username).first():
            messages.info(request,"No User Found with this Phone Number.")
            return redirect('forgetpassword')
        
        user=User.objects.get(username=username)
        token=str(uuid.uuid4())
        profile_obj=Profile.objects.get(user=user)
        profile_obj.forget_password_token=token
        profile_obj.save()
        print(user.email)
        send_forget_password_mail(user.email,token)
        messages.info(request,"Email Send To Your Register Email ID.")
        return redirect('forgetpassword')
            
    return render (request,'forgetpassword.html')

def ResetPassword(request, token):
    context={
        
    }
    profile_obj=Profile.objects.filter(forget_password_token=token).first()
    print(profile_obj)
    context={'user_id': profile_obj.user.id}
    
    if request.method=="POST":
        newpassword=request.POST.get("newpassword")
        cpassword=request.POST.get("cpassword")
        user_id=request.POST.get('user_id')
        
        if user_id is None:
            messages.info(request,"No User Found!!.")
            return redirect(f'resetpassword/<token>/')
        
        if newpassword != cpassword:
            messages.info(request,"Both Password Should be same..")
            return redirect(f'resetpassword/<token>/')
        
        user_obj=User.objects.get(id=user_id)
        user_obj.set_password(newpassword)
        user_obj.save()
        messages.info(request,"Password Change Sucessfully")
        return redirect('login')
    
    
    return render(request,'resetpassword.html',context)




@login_required(login_url='/')
def Home(request):
    img=Images.objects.all()
    numbers=DailyBazar.objects.all()
    Time=DailyTime.objects.all()
    data={
        'img': img,
        'number':numbers,
        'Time': Time
        
    }
    return render(request,'index.html',data)

def Wallet(request):
    point=POINTS.objects.filter(user=request.user)
    return render (request,'wallet.html',{"point":point})

def Bank(request,):
    bank=MANAGEBANK.objects.filter(user=request.user)
    print(bank)
    data={
        'bank':bank
    }
    if request.method == "POST":
        user=request.user
        GooglePayNumber=request.POST.get('GooglePayNumber')
        PhonePayNumber=request.POST.get('PhonePayNumber')
        PayTmNUmber=request.POST.get('PayTmNUmber')
        addbank=MANAGEBANK(user=user,GooglePayNumber=GooglePayNumber,PhonePayNumber=PhonePayNumber,PayTmNUmber=PayTmNUmber)
        addbank.save()
        messages.info(request,"All Details Are save")
    return render (request,'manage_bank.html',data)

def Winning(request):
    
    return render (request,'winning_history.html')

def BID(request):
        data=User.objects.all()
        data1=Milan_MorningFullSangam.objects.all()
        context={  
            'data': data,
            'data1':data1
        }  
        return render (request,'bid_history.html',context)
   

def GamesRate(request):
    return render (request,'games_rate.html')

def Conatct(request):
    return render (request,'contact.html')

def ChangePassword(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            v=form.save()
            update_session_auth_hash(request,v)
            messages.info(request,"Password Change Sucessfully..")
    else:  
        form=PasswordChangeForm(request.user)
    parmas={
        'form': form
    }
    return render (request,'change_password.html',parmas)


def HowToPlay(request):
    return redirect('https://www.youtube.com')

def ADDPOINT(request):
    if request.method=="POST":
        user=request.user
        amount=int(request.POST.get('amount'))*100
        print(amount,user)
        client=razorpay.Client(auth=("rzp_test_WYJiWly9dl8E6t" ,"z5S2phbuGWzBTghHxk8GqBjz"))
        payment=client.order.create({'amount' :amount,'currency': 'INR','payment_capture':'1'})
        # print(payment)
        # a=amount/100
        # userpoint=POINTS(points=a)
        # userpoint.save()
        return render (request,'add_point.html',{'payment': payment})
       
    return render (request,'add_point.html')

def Success(request):
    if request.method=="POST":
        a=request.POST
        print(a)
    return render (request,"success.html")

def STARLINE(request):
    number=Starline.objects.all()
    Time=StarlineTime.objects.all()
    data={
        'number': number,
        'Time': Time
    }
    return render (request,'starline.html',data)

def GALIDISWAR(request):
    number=GaliDisawar.objects.all()
    Time=GaliDisawarTime.objects.all()
    data={
        'number': number,
        'Time': Time   
        }
    return render (request,'galidiswar.html',data)
# sidebar end
# MILAN MORNING START
def MILANMORING(request):
   
    return render (request,'MILANMORNING/millanmoring.html')

def MILANMORNINGSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        milanmorningsingledigit=Milan_MorningSingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        milanmorningsingledigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
    return render (request,'MILANMORNING/single_digit.html')

def MILANMORNINGJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        milanmorningjodidigit=Milan_MorningJodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        milanmorningjodidigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
     return render (request,'MILANMORNING/jodi_digit.html')

def MILANMORNINGSINGLEPANNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        milanmorningsinglepana=Milan_MorningSinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        milanmorningsinglepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
    return render (request,'MILANMORNING/singlepanna.html')

def MILANMORNINGDOUBLEPANNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        milanmorningdoublepana=Milan_MorningDoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        milanmorningdoublepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
    return render (request,'MILANMORNING/doublepanna.html')

def MILANMORNINGTRIPLEPANNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        milanmorningtriplepana=Milan_MorningTriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        milanmorningtriplepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
    return render (request,'MILANMORNING/triplepanna.html')

def MILANMORNINGHALFSANGAM(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        milanmorninghalfsangam=Milan_MorningHalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        milanmorninghalfsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
    return render (request,'MILANMORNING/halfsangam.html')

def MILANMORNINGFULLSANGAM(request):
    if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        milanmorningfullsangam=Milan_MorningFullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        milanmorningfullsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milan_morning')
    return render (request,'MILANMORNING/fullsangam.html')
# MILAN MORNING END
# WELCOMR MORNING START
def WELCOMEMORNING(request):
    return render (request,'WELCOMEMORING/welcomemorning.html')

def WELCOMEMORNINGSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        welcomemorningsingledigit=Welcome_MorningSingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        welcomemorningsingledigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/welcomesingle_digit.html')

def WELCOMEMORNINGJODIDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        welcomemorningjodidigit=Welcome_MorningJodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        welcomemorningjodidigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/welcomejodi_digit.html')

def WELCOMEMORNINGSINGLEPANNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        welcomemorningsinglepana=Welcome_MorningSinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        welcomemorningsinglepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/singlepanna.html')

def WELCOMEMORNINGDOUBLEPANNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        welcomemorningdoublepana=Welcome_MorningDoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        welcomemorningdoublepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/doublepanna.html')

def WELCOMEMORNINGTRIPLEPANNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        welcomemorningtriplepana=Welcome_MorningTriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        welcomemorningtriplepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/triplepanna.html')

def WELCOMEMORNINGHALFSANGAM(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        welcomemorninghalfsangam=Welcome_MorningHalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        welcomemorninghalfsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/halfsangam.html')

def WELCOMEMORNINGFULLSANGAM(request):
    if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        welcomemorningfullsangam=Welcome_MorningFullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        welcomemorningfullsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('welcome_morning')
    return render (request,'WELCOMEMORING/fullsangam.html')
# WELCOME MORNING END
# KALYAN MORNING START
def KALYANMORNING(request):
    return render (request,'KALYANMORNING/kalyanmorning.html')

def KALYANMORINGSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        kalyanmorningsingledigit=Kalyan_MorningSingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        kalyanmorningsingledigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
     return render (request,'KALYANMORNING/single_digit.html')

def KALYANMORINGJODIDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        kalyanmorningjodidigit=Kalyan_MorningJodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        kalyanmorningjodidigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
    return render (request,'KALYANMORNING/jodi_digit.html')

def KALYANMORINGSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        kalyanmorningsinglepana=Kalyan_MorningSinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        kalyanmorningsinglepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
    return render (request,'KALYANMORNING/singlepanna.html')

def KALYANMORINGDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        kalyanmorningdoublepana=Kalyan_MorningDoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        kalyanmorningdoublepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
    return render (request,'KALYANMORNING/doublepanna.html')

def KALYANMORNINGTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        kalyanmorningtriplepana=Kalyan_MorningTriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        kalyanmorningtriplepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
    return render (request,'KALYANMORNING/triplepanna.html')

def KALYANMORINGJHALFSANGAM(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        kalyanmorninghalfsangam=Kalyan_MorningHalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        kalyanmorninghalfsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
    return render (request,'KALYANMORNING/halfsangam.html')

def KALYANMORINGFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        kalyanmorningfullsangam=Kalyan_MorningFullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        kalyanmorningfullsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan_morning')
     return render (request,'KALYANMORNING/fullsangam.html')
# KALYAN MORNING END
# MADHUR MORNING START
def MADHURMORNING(request):
    return render (request,'MADHURMORNING/madhurmorning.html')

def MADHURMORNINGSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        madhurmorningsingledigit=Madhur_MorningSingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        madhurmorningsingledigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
     return render (request,'MADHURMORNING/single_digit.html')

def MADHURMORINGJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        madhurmorningjodidigit=Madhur_MorningJodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        madhurmorningjodidigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
     return render (request,'MADHURMORNING/jodi_digit.html')

def MADHURMORINGSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        madhurmorningsinglepana=Madhur_MorningSinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        madhurmorningsinglepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
    return render (request,'MADHURMORNING/singlepanna.html')

def MADHURMORINGDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        madhurmorningdoublepana=Madhur_MorningDoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        madhurmorningdoublepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
    return render (request,'MADHURMORNING/doublepanna.html')

def MADHURMORINGTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        madhurmorningtriplepana=Madhur_MorningTriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        madhurmorningtriplepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
    return render (request,'MADHURMORNING/triplepanna.html')

def MADHURMORINGHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        madhurmorninghalfsangam=Madhur_MorningHalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        madhurmorninghalfsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
     return render (request,'MADHURMORNING/halfsangam.html')

def MADHURMORINGFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        madhurmorningfullsangam=Madhur_MorningFullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        madhurmorningfullsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhur_morning')
     return render (request,'MADHURMORNING/fullsangam.html')
# MADHUR MORING END
# SRIDEVI START
def SRIDEVI(request):
    return render (request,'SRIDEVI/sridevi.html')

def SRIDEVISINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        siridevisingledigit=SrideviSingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        siridevisingledigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
     return render (request,'SRIDEVI/single_digit.html')

def SRIDEVIJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        sridevijodidigit=SrideviJodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        sridevijodidigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
     return render (request,'SRIDEVI/jodi_digit.html')

def SRIDEVISINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sridevisinglepana=Kalyan_MorningSinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sridevisinglepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
    return render (request,'SRIDEVI/singlepanna.html')

def SRIDEVIDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sridevidoublepana=SrideviDoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sridevidoublepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
    return render (request,'SRIDEVI/doublepanna.html')

def SRIDEVITRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sridevitriplepana=SrideviTriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sridevitriplepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
    return render (request,'SRIDEVI/triplepanna.html')

def SRIDEVIHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        sridevihalfsangam=SrideviHalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        sridevihalfsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
     return render (request,'SRIDEVI/halfsangam.html')

def SRIDEVIFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        sridevifullsangam=SrideviFullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        sridevifullsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevi')
     return render (request,'SRIDEVI/fullsangam.html')
# SRIDEVI END
# TIMEBAZAR START
def TIMEBAZAR(request):
    return render (request,'TIMEBAZAR/timebazar.html')

def TIMEBAZARSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        timebazarsingledigit=Time_Bazar_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        timebazarsingledigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
     return render (request,'TIMEBAZAR/single_digit.html')

def TIMEBAZARJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        timebazarjodidigit=Time_Bazar_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        timebazarjodidigit.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
     return render (request,'TIMEBAZAR/jodi_digit.html')

def TIMEBAZARSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        timebazarsinglepana=Time_Bazar_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        timebazarsinglepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
    return render (request,'TIMEBAZAR/singlepanna.html')

def TIMEBAZARDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        timebazardoublepana=Time_Bazar_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        timebazardoublepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
    return render (request,'TIMEBAZAR/doublepanna.html')

def TIMEBAZARTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        timebazartriplepana=Time_Bazar_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        timebazartriplepana.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
    return render (request,'TIMEBAZAR/triplepanna.html')

def TIMEBAZARHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        timebazarhalfsangam=Time_Bazar_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        timebazarhalfsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
     return render (request,'TIMEBAZAR/halfsangam.html')

def TIMEBAZARFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        timebazarfullsangam=Time_Bazar_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        timebazarfullsangam.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('timebazar')
     return render (request,'TIMEBAZAR/fullsangam.html')
# TIMEBAZAR END
#  MADHUR DAY START
def MADHURDAY(request):
    return render (request,'MADHURDAY/madhurday.html')

def MADHURDAYSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mds=Madhur_Day_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        mds.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
     return render (request,'MADHURDAY/single_digit.html')

def MADHURDAYJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mdj=Madhur_Day_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        mdj.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
     return render (request,'MADHURDAY/jodi_digit.html')

def MADHURDAYSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mdsp=Madhur_Day_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mdsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
    return render (request,'MADHURDAY/singlepanna.html')

def MADHURDAYDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mddp=Madhur_Day_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mddp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
    return render (request,'MADHURDAY/doublepanna.html')

def MADHURDAYTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mdtp=Madhur_Day_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mdtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
    return render (request,'MADHURDAY/triplepanna.html')

def MADHURDAYHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mdhs=Madhur_Day_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        mdhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
     return render (request,'MADHURDAY/halfsangam.html')

def MADHURDAYFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mdfs=Madhur_Day_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        mdfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurday')
     return render (request,'MADHURDAY/fullsangam.html')
#  MADHUR DAY END
#  NEW KALYAN START
def NEWKALYAN(request):
    return render (request,'NEWKALYAN/newkalyan.html')

def NEWKALYANSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        nksd=New_Kalyan_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        nksd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
     return render (request,'NEWKALYAN/single_digit.html')

def NEWKALYANJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        nkjd=New_Kalyan_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        nkjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
     return render (request,'NEWKALYAN/jodi_digit.html')

def NEWKALYANSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        nksp=New_Kalyan_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        nksp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
    return render (request,'NEWKALYAN/singlepanna.html')

def NEWKALYANDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        nkdp=New_Kalyan_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        nkdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
    return render (request,'NEWKALYAN/doublepanna.html')

def NEWKALYANTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        nktp=New_Kalyan_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        nktp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
    return render (request,'NEWKALYAN/triplepanna.html')

def NEWKALYANHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        nkhs=New_Kalyan_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        nkhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
     return render (request,'NEWKALYAN/halfsangam.html')

def NEWKALYANFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        nkfs=New_Kalyan_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        nkfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newkalyan')
     return render (request,'NEWKALYAN/fullsangam.html')
#  NEW KALYAN END
#  MILANDAY START
def MILANDAY(request):
    return render (request,'MILANDAY/milanday.html')

def MILANDAYSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mdsd=Milan_Day_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        mdsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
     return render (request,'MILANDAY/single_digit.html')

def MILANDAYJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        msjd=Milan_Day_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        msjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
     return render (request,'MILANDAY/jodi_digit.html')

def MILANDAYSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mdsp=Milan_Day_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mdsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
    return render (request,'MILANDAY/singlepanna.html')

def MILANDAYDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mddp=Milan_Day_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mddp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
    return render (request,'MILANDAY/doublepanna.html')

def MILANDAYTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mdtp=Milan_Day_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mdtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
    return render (request,'MILANDAY/triplepanna.html')

def MILANDAYHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mdhs=Milan_Day_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        mdhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
     return render (request,'MILANDAY/halfsangam.html')

def MILANDAYFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mdfs=Madhur_Day_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        mdfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milanday')
     return render (request,'MILANDAY/fullsangam.html')
# MILANDAY END
# RAJDHANI DAY
def RAJDHANIDAY(request):
    return render (request,'RAJDHANIDAY/rajdhaniday.html')

def RAJDHANIDAYSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        rdsd=Rajdhani_Day_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        rdsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
     return render (request,'RAJDHANIDAY/single_digit.html')

def RAJDHANIDAYJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        rdjd=Rajdhani_Day_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        rdjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
     return render (request,'RAJDHANIDAY/jodi_digit.html')

def RAJDHANIDAYJSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        rdsp=Rajdhani_Day_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        rdsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
    return render (request,'RAJDHANIDAY/singlepanna.html')

def RAJDHANIDAYDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        rddp =Rajdhani_Day_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        rddp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
    return render (request,'RAJDHANIDAY/doublepanna.html')

def RAJDHANIDAYTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        rdtp=Rajdhani_Day_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        rdtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
    return render (request,'RAJDHANIDAY/triplepanna.html')

def RAJDHANIDAYHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        rdhs =Rajdhani_Day_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        rdhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
     return render (request,'RAJDHANIDAY/halfsangam.html')

def RAJDHANIDAYFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        rdfs=Rajdhani_Day_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        rdfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaniday')
     return render (request,'RAJDHANIDAY/fullsangam.html')
# RAJDHANI DAY END
# SUPREME DAY START
def SUPREMEDAY(request):
    return render (request,'SUPREMEDAY/supremeday.html')

def SUPREMEDAYSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        sdsd=Supreme_Day_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        sdsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
     return render (request,'SUPREMEDAY/single_digit.html')

def SUPREMEDAYJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        sdjd=Supreme_Day_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        sdjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
     return render (request,'SUPREMEDAY/jodi_digit.html')

def SUPREMEDAYSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sdsp=Supreme_Day_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sdsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
    return render (request,'SUPREMEDAY/singlepanna.html')

def SUPREMEDAYDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sddp=Supreme_Day_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sddp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
    return render (request,'SUPREMEDAY/doublepanna.html')

def SUPREMEDAYTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sdtp=Supreme_Day_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sdtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
    return render (request,'SUPREMEDAY/triplepanna.html')

def SUPREMEDAYHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        sdhs=Supreme_Day_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        sdhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
     return render (request,'SUPREMEDAY/halfsangam.html')

def SUPREMEDAYFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        sdfs=Supreme_Day_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        sdfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremeday')
     return render (request,'SUPREMEDAY/fullsangam.html')
# SUPREME DAY END
# KALYAN START
def KALYAN(request):
    return render (request,'KALYAN/kalyan.html')

def KALYANSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        ksd =Kalyan_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        ksd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
     return render (request,'KALYAN/single_digit.html')

def KALYANJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        kjd=Kalyan_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        kjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
     return render (request,'KALYAN/jodi_digit.html')

def KALYANSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        ksp=Kalyan_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        ksp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
    return render (request,'KALYAN/singlepanna.html')

def KALYANDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        kdp=Kalyan_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        kdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
    return render (request,'KALYAN/doublepanna.html')

def KALYANTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        ktp =Kalyan_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        ktp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
    return render (request,'KALYAN/triplepanna.html')

def KALYANHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        khs=Kalyan_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        khs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
     return render (request,'KALYAN/halfsangam.html')

def KALYANFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        kfs=Kalyan_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        kfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyan')
     return render (request,'KALYAN/fullsangam.html')
# KALYAN END

# SRIDEVI NIGHT START
def SRIDEVINIGHT(request):
    return render (request,'SRIDEVINIGHT/sridevinight.html')

def SRIDEVINIGHTSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        snsd=Sridevi_Night_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        snsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
     return render (request,'SRIDEVINIGHT/single_digit.html')

def SRIDEVINIGHTJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        snjd=Sridevi_Night_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        snjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
     return render (request,'SRIDEVINIGHT/jodi_digit.html')

def SRIDEVINIGHTSINGLEPAMNA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        snsp=Sridevi_Night_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        snsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
    return render (request,'SRIDEVINIGHT/singlepanna.html')

def SRIDEVINIGHTDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sndp=Sridevi_Night_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sndp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
    return render (request,'SRIDEVINIGHT/doublepanna.html')

def SRIDEVINIGHTTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sntp=Sridevi_Night_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sntp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
    return render (request,'SRIDEVINIGHT/triplepanna.html')

def SRIDEVINIGHTHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        snhs=Sridevi_Night_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        snhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
     return render (request,'SRIDEVINIGHT/halfsangam.html')

def SRIDEVINIGHTFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        snfs=Sridevi_Night_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        snfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('sridevinight')
     return render (request,'SRIDEVINIGHT/fullsangam.html')
# SRIDEVI NIGHT END
# MADHUR NIGHT START
def MADHURINIGHT(request):
    return render (request,'MADHURNIGHT/madhurnight.html')

def MADHURNIGHTSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mnsd =Madhur_Night_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        mnsd .save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
     return render (request,'MADHURNIGHT/single_digit.html')

def MADHURNIGHTJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mnjd=Madhur_Night_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        mnjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
     return render (request,'MADHURNIGHT/jodi_digit.html')

def MADHURNIGHTSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mnsp =Madhur_Night_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mnsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
    return render (request,'MADHURNIGHT/singlepanna.html')

def MADHURNIGHTDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mndp=Madhur_Night_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mndp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
    return render (request,'MADHURNIGHT/doublepanna.html')

def MADHURNIGHTTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mntp=Madhur_Night_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mntp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
    return render (request,'MADHURNIGHT/triplepanna.html')

def MADHURNIGHTHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mnhs =Madhur_Night_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        mnhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
     return render (request,'MADHURNIGHT/halfsangam.html')

def MADHURNIGHTFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mnfs=Madhur_Night_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        mnfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('madhurnight')
     return render (request,'MADHURNIGHT/fullsangam.html')
# MADHRU NIGHT END
# NEW MUMBAI START
def NEWMAINMUMBAI(request):
    return render (request,'NEWMAINMUMBAI/newmainmumbai.html')

def NEWMAINMUMBAISINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        nmmsj=New_Main_Mumbai_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        nmmsj.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
     return render (request,'NEWMAINMUMBAI/single_digit.html')

def NEWMAINMUMBAIJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mnmjd =New_Main_Mumbai_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        mnmjd .save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
     return render (request,'NEWMAINMUMBAI/jodi_digit.html')

def NEWMAINMUMBAISINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mnmsp=New_Main_Mumbai_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mnmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
    return render (request,'NEWMAINMUMBAI/singlepanna.html')

def NEWMAINMUMBAIDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mnmdp=New_Main_Mumbai_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mnmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
    return render (request,'NEWMAINMUMBAI/doublepanna.html')

def NEWMAINMUMBAITRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mnmtp=New_Main_Mumbai_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mnmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
    return render (request,'NEWMAINMUMBAI/triplepanna.html')

def NEWMAINMUMBAIHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mnmhs=New_Main_Mumbai_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        mnmhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
     return render (request,'NEWMAINMUMBAI/halfsangam.html')

def NEWMAINMUMBAIFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mnmfs=New_Main_Mumbai_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        mnmfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('newmainmumbai')
     return render (request,'NEWMAINMUMBAI/fullsangam.html')
# NEW MAIN MUMBAI END
# SUPREME NIGHT START
def SUPREMENIGHT(request):
    return render (request,'SUPREMENIGHT/supremenight.html')

def SUPREMENIGHTSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        snsd=Supreme_Night_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        snsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
     return render (request,'SUPREMENIGHT/single_digit.html')

def SUPREMENIGHTJODIDIGIT(request):
      if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        snjd=Supreme_Night_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        snjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
      return render (request,'SUPREMENIGHT/jodi_digit.html')

def SUPREMENIGHTSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        snsp=Supreme_Night_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        snsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
    return render (request,'SUPREMENIGHT/singlepanna.html')

def SUPREMENIGHTDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sndp=Supreme_Night_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sndp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
    return render (request,'SUPREMENIGHT/doublepanna.html')

def SUPREMENIGHTTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sntp=Supreme_Night_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        sntp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
    return render (request,'SUPREMENIGHT/triplepanna.html')

def SUPREMENIGHTHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        snhs=Supreme_Night_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        snhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
     return render (request,'SUPREMENIGHT/halfsangam.html')

def SUPREMENIGHTFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        snfs =Supreme_Night_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        snfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('supremenight')
     return render (request,'SUPREMENIGHT/fullsangam.html')
# SUPREME NIGHT END
# MILAN NIGHT START
def MILANNIGHT(request):
    return render (request,'MILANNIGHT/milannight.html')

def MILANNIGHTSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mnsd=Milan_Night_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        mnsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
     return render (request,'MILANNIGHT/single_digit.html')

def MILANNIGHTJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mnjd=Milan_Night_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        mnjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
     return render (request,'MILANNIGHT/jodi_digit.html')

def MILANNIGHTSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mnsp=Milan_Night_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mnsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
    return render (request,'MILANNIGHT/singlepanna.html')

def MILANNIGHTDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mndp=Milan_Night_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mndp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
    return render (request,'MILANNIGHT/doublepanna.html')

def MILANNIGHTJTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mntp=Milan_Night_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mntp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
    return render (request,'MILANNIGHT/triplepanna.html')

def MILANNIGHTHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mnhs=Milan_Night_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        mnhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
     return render (request,'MILANNIGHT/halfsangam.html')

def MILANNIGHTFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mnfs=Milan_Night_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        mnfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('milannight')
     return render (request,'MILANNIGHT/fullsangam.html')
# MILAN NIGHT END
# KALYAN NIGHT START
def KALYANNIGHT(request):
    return render (request,'KALYANNIGHT/kalyannight.html')

def KALYANNIGHTSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        knsd=Kalyan_Night_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        knsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
     return render (request,'KALYANNIGHT/single_digit.html')

def KALYANNIGHTJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        knjd=Kalyan_Night_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        knjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
     return render (request,'KALYANNIGHT/jodi_digit.html')

def KALYANNIGHTSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        knsp=Kalyan_Night_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        knsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
    return render (request,'KALYANNIGHT/singlepanna.html')

def KALYANNIGHTDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        kndp=Kalyan_Night_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        kndp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
    return render (request,'KALYANNIGHT/doublepanna.html')

def KALYANNIGHTTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        kntp=Kalyan_Night_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        kntp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
    return render (request,'KALYANNIGHT/triplepanna.html')

def KALYANNIGHTHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        knhs=Kalyan_Night_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        knhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
     return render (request,'KALYANNIGHT/halfsangam.html')

def KALYANNIGHTFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        knfs=Kalyan_Night_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        knfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('kalyannight')
     return render (request,'KALYANNIGHT/fullsangam.html')
# KALYAN NIGHT END
# RAJDHANI NIGHT START
def RAJDHANINIGHT(request):
    return render (request,'RAJADHANINIGHT/rajadhaninight.html')

def RAJDHANINIGHTSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        rjnsd=Rajdhani_Night_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        rjnsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
     return render (request,'RAJADHANINIGHT/single_digit.html')

def RAJDHANINIGHTJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        rjnjd=Rajdhani_Night_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        rjnjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
     return render (request,'RAJADHANINIGHT/jodi_digit.html')

def RAJDHANINIGHTSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        rjnsp=Rajdhani_Night_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        rjnsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
    return render (request,'RAJADHANINIGHT/singlepanna.html')

def RAJDHANINIGHTDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        rjndp=Rajdhani_Night_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        rjndp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
    return render (request,'RAJADHANINIGHT/doublepanna.html')

def RAJDHANINIGHTTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        rjntp=Rajdhani_Night_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        rjntp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
    return render (request,'RAJADHANINIGHT/triplepanna.html')

def RAJDHANINIGHTHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        rjnhs=Rajdhani_Night_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        rjnhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
     return render (request,'RAJADHANINIGHT/halfsangam.html')

def RAJDHANINIGHTFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        rjnfs=Rajdhani_Night_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        rjnfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('rajdhaninight')
     return render (request,'RAJADHANINIGHT/fullsangam.html')
# RAJDHANI NIGHT START
# MAIN BAZAR START
def MAINBAZAR(request):
    return render (request,'MAINBAZAR/mainbazar.html')

def MAINBAZARSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mbsd=Main_Bazar_SingleDigit(user=user,session=session,digit=digit,points=points,date=datetime.today())
        mbsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
     return render (request,'MAINBAZAR/single_digit.html')

def MAINBAZARJODIDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        mbjd=Main_Bazar_JodiDigit(user=user,digit=digit,points=points,date=datetime.today())
        mbjd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
     return render (request,'MAINBAZAR/jodi_digit.html')

def MAINBAZARSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mbsp=Main_Bazar_SinglePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mbsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
    return render (request,'MAINBAZAR/singlepanna.html')

def MAINBAZARDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mbdp=Main_Bazar_DoublePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mbdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
    return render (request,'MAINBAZAR/doublepanna.html')

def MAINBAZARTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        mbtp=Main_Bazar_TriplePana(user=user,session=session,pana=pana,points=points,date=datetime.today())
        mbtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
    return render (request,'MAINBAZAR/triplepanna.html')

def MAINBAZARHALFSANGAM(request):
     if request.method=="POST":
        user=request.user
        session=request.POST.get('session')
        open_digit=request.POST.get('open_digit')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mbhs=Main_Bazar_HalfSangam(user=user,session=session,open_digit=open_digit,close_pana=close_pana,points=points,date=datetime.today())
        mbhs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
     return render (request,'MAINBAZAR/halfsangam.html')

def MAINBAZARFULLSANGAM(request):
     if request.method=="POST":
        user=request.user
        open_pana=request.POST.get('open_pana')
        close_pana=request.POST.get('close_pana')
        points=request.POST.get('points')
        mbfs=Main_Bazar_FullSangam(user=user,open_pana=open_pana,close_pana=close_pana,points=points,date=datetime.today())
        mbfs.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('mainbazar')
     return render (request,'MAINBAZAR/fullsangam.html')
# MAIN BAZAR END
# STARLINE TIME 
def TENAM(request):
    return render (request,'STARLINE/10am.html')
def ELEVENAM(request):
    return render (request,'STARLINE/11am.html')
def TWELEPM(request):
    return render (request,'STARLINE/12pm.html')
def ONEPM(request):
    return render (request,'STARLINE/01pm.html')
def TWOPM(request):
    return render (request,'STARLINE/02pm.html')
def THREEPM(request):
    return render (request,'STARLINE/03pm.html')
def FOURPM(request):
    return render (request,'STARLINE/04pm.html')
def FIVEPM(request):
    return render (request,'STARLINE/05pm.html')
def SIXPM(request):
    return render (request,'STARLINE/06pm.html')
def SEVEANPM(request):
    return render (request,'STARLINE/07pm.html')
def EIGHTPM(request):
    return render (request,'STARLINE/08pm.html')
def NINEPM(request):
    return render (request,'STARLINE/09pm.html')
def TENPM(request):
    return render (request,'STARLINE/10pm.html')
# STARLINE TIME END
# 10:00 AM START
def TENAMSINGLEDIGIT(request):
     if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        tenamsd=Ten_AM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        tenamsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10am')
     return render (request,'10AM/singledigit.html')
def TENAMSINGLEPANA(request):
     if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tenamsp=Ten_AM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        tenamsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10am')
     return render (request,'10AM/singlepana.html')
def TENAMDOUBLEPANA(request):
     if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tenamdp=Ten_AM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        tenamdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10am')
     return render (request,'10AM/doublepana.html')
def TENAMTRIPLEPANA(request):
     if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tenamtp=Ten_AM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        tenamtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10am')
     return render (request,'10AM/triplepana.html')
# 11AM START
def ELEVENAMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        eamsd=Eleven_AM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        eamsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('11am')
    return render (request,'11AM/singledigit.html')

def ELEVENAMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        eamsp=Eleven_AM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        eamsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('11am')
    return render (request,'11AM/singlepana.html')

def ELEVENAMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        eamdp=Eleven_AM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        eamdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('11am')
    return render (request,'11AM/doublepana.html')

def ELEVENAMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        eamtp=Eleven_AM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        eamtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('11am')
    return render (request,'11AM/triplepana.html')
# 12PM
def TWELEPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        tvelpmsd=Twelve_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        tvelpmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('12pm')
    return render (request,'12PM/singledigit.html')

def TWELEPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tvelpmsp=Twelve_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        tvelpmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('12pm')
    return render (request,'12PM/singlepana.html')

def TWELEPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tvelpmdp=Twelve_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        tvelpmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('12pm')
    return render (request,'12PM/doublepana.html')

def TWELEPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tvelpmtp=Twelve_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        tvelpmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('12pm')
    return render (request,'12PM/triplepana.html')
# 01PM
def ONEPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        onepmsd=One_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        onepmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('01pm')
    return render (request,'01PM/singledigit.html')

def ONEPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        onepmsp=One_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        onepmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('01pm')
    return render (request,'01PM/singlepana.html')

def ONEPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        onepmdp=One_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        onepmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('01pm')
    return render (request,'01PM/doublepana.html')

def ONEPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        onepmtp=One_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        onepmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('01pm')
    return render (request,'01PM/triplepana.html')
# 02PM
def TWOPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        twopmsd=Two_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        twopmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('02pm')
    return render (request,'02PM/singledigit.html')

def TWOPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        twopmsp=Two_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        twopmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('02pm')
    return render (request,'02PM/singlepana.html')

def TWOPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        twopmdp=Two_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        twopmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('02pm')
    return render (request,'02PM/doublepana.html')

def TWOPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        twopmtp=Two_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        twopmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('02pm')
    return render (request,'02PM/triplepana.html')
# 03PM
def THREEPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        threepmsd=Three_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        threepmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('03pm')
    return render (request,'03PM/singledigit.html')

def THREEPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        threepmsp=Three_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        threepmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('03pm')
    return render (request,'03PM/singlepana.html')

def THREEPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        threepmdp=Three_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        threepmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('03pm')
    return render (request,'03PM/doublepana.html')

def THREEPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        threepmtp=Three_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        threepmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('03pm')
    return render (request,'03PM/triplepana.html')
# 04PM
def FOURPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        fourpmsd=Four_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        fourpmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('04pm')
    return render (request,'04PM/singledigit.html')

def FOURPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        fourpmsp=Four_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        fourpmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('04pm')
    return render (request,'04PM/singlepana.html')

def FOURPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        fourpmdp=Four_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        fourpmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('04pm')
    return render (request,'04PM/doublepana.html')

def FOURPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        fourpmtp=Four_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        fourpmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('04pm')
    return render (request,'04PM/triplepana.html')
# 05 PM
def FIVEPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        fivepmsd=Five_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        fivepmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('05pm')
    return render (request,'05PM/singledigit.html')

def FIVEPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        fivepmsp=Five_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        fivepmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('05pm')
    return render (request,'05PM/singlepana.html')

def FIVEPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        fivepmdp=Five_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        fivepmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('05pm')
    return render (request,'05PM/doublepana.html')

def FIVEPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        fivepmtp=Five_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        fivepmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('05pm')
    return render (request,'05PM/triplepana.html')
# 06PM
def SIXPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        sixpmsd=Six_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        sixpmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('06pm')
    return render (request,'06PM/singledigit.html')

def SIXPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sixpmsp=Six_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        sixpmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('06pm')
    return render (request,'06PM/singlepana.html')

def SIXPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sixpmdp=Six_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        sixpmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10am')
    return render (request,'06PM/doublepana.html')

def SIXPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sixpmtp=Six_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        sixpmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('06pm')
    return render (request,'06PM/triplepana.html')
# 07PM
def SEVENPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        sevenpmsd=Seven_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        sevenpmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('07pm')
    return render (request,'07PM/singledigit.html')

def SEVENPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sevenpmsp=Seven_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        sevenpmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('07pm')
    return render (request,'07PM/singlepana.html')

def SEVENPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sevenpmdp=Seven_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        sevenpmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('07pm')
    return render (request,'07PM/doublepana.html')

def SEVENPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        sevenpmtp=Seven_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        sevenpmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('07pm')
    return render (request,'07PM/triplepana.html')
# 08PM
def EIGHTPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        eightpmsd=Eight_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        eightpmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('08pm')
    return render (request,'08PM/singledigit.html')

def EIGHTPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        eightpmsp=Eight_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        eightpmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('08pm')
    return render (request,'08PM/singlepana.html')

def EIGHTPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        eightpmdp=Eight_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        eightpmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('08pm')
    return render (request,'08PM/doublepana.html')

def EIGHTPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        eightpmtp=Eight_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        eightpmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('08pm')
    return render (request,'08PM/triplepana.html')
# 09PM
def NINEPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        ninepmsd=Nine_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        ninepmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('09pm')
    return render (request,'09PM/singledigit.html')

def NINEPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        ninepmsp=Nine_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        ninepmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('09pm')
    return render (request,'09PM/singlepana.html')

def NINEPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        ninepmdp=Nine_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        ninepmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('09pm')
    return render (request,'09PM/doublepana.html')

def NINEPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        ninepmtp=Nine_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        ninepmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('09pm')
    return render (request,'09PM/triplepana.html')
# 10PM
def TENPMSINGLEDIGIT(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        tenpmsd=Ten_PM_SingleDigit(user=user,digit=digit,points=points,date=datetime.today())
        tenpmsd.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10pm')
    return render (request,'10PM/singledigit.html')

def TENPMSINGLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tenpmsp=Ten_PM_SinglePana(user=user,pana=pana,points=points,date=datetime.today())
        tenpmsp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10pm')
    return render (request,'10PM/singlepana.html')

def TENPMDOUBLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tenpmdp=Ten_PM_DoublePana(user=user,pana=pana,points=points,date=datetime.today())
        tenpmdp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10pm')
    return render (request,'10PM/doublepana.html')

def TENPMTRIPLEPANA(request):
    if request.method=="POST":
        user=request.user
        pana=request.POST.get('pana')
        points=request.POST.get('points')
        tenpmtp=Ten_PM_TriplePana(user=user,pana=pana,points=points,date=datetime.today())
        tenpmtp.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('10pm')
    return render (request,'10PM/triplepana.html')
# GALIDISAWAR
def DISAWAR(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        dis=Disawar(user=user,digit=digit,points=points,date=datetime.today())
        dis.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('disawar')
    return render (request,'Galidisawar/disawar.html')

def FARIDABAAD(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        faridabad=Faridabaad(user=user,digit=digit,points=points,date=datetime.today())
        faridabad.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('faribadaad')
    return render (request,'Galidisawar/faridabaad.html')

def GAZIABAAD(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        gaziabad=Gaziabaad(user=user,digit=digit,points=points,date=datetime.today())
        gaziabad.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('gaziabaad')
    return render (request,'Galidisawar/gaziabaad.html')

def GALI(request):
    if request.method=="POST":
        user=request.user
        digit=request.POST.get('digit')
        points=request.POST.get('points')
        gali=Gali(user=user,digit=digit,points=points,date=datetime.today())
        gali.save()
        messages.info(request,"Your Bid Recived.Thank You!! ")
        return redirect('gali')
    return render (request,'Galidisawar/gali.html')



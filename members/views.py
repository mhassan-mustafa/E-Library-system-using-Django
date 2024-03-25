from django.shortcuts import render, redirect, reverse
from .models import *
from admins.models import Books
from .decorators import member_login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import random
import os


@member_login_required
def home(request):
    title = "Home Page"
    
    if request.user.is_authenticated and request.user.is_member:
        books = Books.objects.all()
        search = False
        
        if request.GET.get('search'):
            search = True
            books = books.filter(title__icontains = request.GET.get('search'))
            
        
        qty = len(books)
        return render(request, "members/home.html", context={"books": books, "quantity": qty, "search": search, "title": title})
    else:
        return redirect("/")  
    

def register(request):
    title = "Register Page"
    
    def generate_verification_code():
        return str(random.randint(100000, 999999))
    
    if request.method == "POST":
        name = request.POST.get('name') 
        email = request.POST.get('email') 
        phone_no = request.POST.get('phone') 
        password = request.POST.get('password')
        
        if not name or not email or not phone_no or not password:
            messages.info(request, "Please fill-out all fields.")
            return render(request, "members/register.html", context = {"title": title, "message_id": 1})
            
        user_email = Members.objects.filter(email = email)
        
        if user_email.exists():
            messages.info(request, "Account with this Email-ID already exist!.")
            return render(request, "members/register.html", context = {"title": title, "message_id": 2})
        
        user = Members.objects.create_user(
            name = name,
            email = email,
            phone_number = phone_no,
            password = password,
            verification_code = generate_verification_code()
        )
        
        email = email.lower()
        verifying_user = Members.objects.get(email = email)


        def send_verification_email(user):
            subject = 'Account Verification'
            message = f'Your verification code is: {user.verification_code}'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]

            send_mail(subject, message, from_email, to_email)
            
        send_verification_email(verifying_user)
        
        account_id = Members.objects.filter(email = email).first().id
        
        url = reverse('members:verify', args = [account_id])    
        return redirect(url)

        
    return render(request, "members/register.html", context = {"title": title})


def verify(request, account_id):
    title = "Verification Page"
    
    if request.method == 'POST':
        code = request.POST.get('code')
        
        user = Members.objects.get(id = account_id)
        
        if code == user.verification_code and not user.is_varified:
            user.is_varified = True
            user.save()
            messages.info(request, "Email varified Successfully, you can login now.")
            return render(request, "members/verify.html", context = {"title": title, "message_id": 1})
        elif user.is_varified:
            messages.info(request, "Account's email is already verified, you can login now.")
        else:
            messages.info(request, "Verification code not match, please try again.")
        
    
    
    return render(request, "members/verify.html", context = {"title": title})


def login_page(request):
    title = "Member Login"
    
    if request.user.is_authenticated and request.user.is_member:
        return render(request, "members/home.html", context = {"title": "Home Page"})
    
    
    if request.method == "POST":
        email = request.POST.get('email') 
        password = request.POST.get('password')
    
        if not email or not password:
            messages.info(request, "Please fill-out all fields.")
            return redirect("/members/login/")

        selected_user = Members.objects.filter(email = email).first()
        
        if not selected_user:
            messages.info(request, "Provided email doesn't exist.")
            return redirect("/members/login/")
        
        user = authenticate(email = email, password = password)
        
        if user == None:
            messages.info(request, "Invalid Password.")
            return redirect("/members/login/")        
        else:
            if selected_user.is_varified == True:
                login(request, user)
                return redirect("/members/home/")
            else:
                messages.info(request, "Can't login, your email is not verified.")
                print(selected_user.id)
                return render(request, "members/login.html", context = {"title": title,"message_id": 1, "account_id": selected_user.id})

      
    return render(request, "members/login.html", context = {"title": title})


@member_login_required
def logout_page(request):
    logout(request)
    return redirect(reverse("members:login"))


@member_login_required
def change_password(request):
    title = "Change Password"
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        if not old_password or not new_password:
            messages.info(request, "Please fill-out all fields.")
            return render(request, "members/change_password.html", context = {"title": title})
        
        email_id = request.user.email
        
        user = Members.objects.get(email = email_id)
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.info(request, "Password Changed Successfully, Login again.")
            return render(request, "members/change_password.html", context = {"title": title})
        
        else:
            messages.info(request, "Old Password is Incorrect.!")
            return render(request, "members/change_password.html", context = {"title": title})
            
    return render(request, "members/change_password.html", context = {"title": title})


@member_login_required
def view(request, book_id):
    title = "View Book"
    
    book = Books.objects.filter(id=book_id).first()
    
    return render(request, "members/view.html", context = {"book": book, "title": title})


@member_login_required
def request_book(request, book_id):
    title = 'Request Book'
    book = Books.objects.filter(id=book_id).first()
    
    user_email = request.user.email
    email_sent = False

    if request.method == 'POST':
        subject = f"Your requested book '{book.title}' from E-Library"
        message = 'Please find the attached Book.'
        from_email = settings.EMAIL_HOST_USER
        to_email = user_email

        email = EmailMessage(subject, message, from_email, [to_email])

        pdf_path = os.path.join(settings.BASE_DIR, 'media', book.pdf.path)
        email.attach_file(pdf_path)

        email.send()
        email_sent = True

    
    return render(request, "members/request_book.html", context = {"title": title, "book": book, "user_email": user_email, "email_sent": email_sent})

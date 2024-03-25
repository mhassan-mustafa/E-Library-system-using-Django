from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import *
from .decorators import admin_login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def index(request):
    title = "Welcome"
    
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("/admin/home/")
        
        if request.user.is_member:
            return redirect("/members/home/")
    
    return render(request, "admins/index.html", context = {"title": title})

@admin_login_required
def home(request):
    title = "Home Page"
    books = Books.objects.all()
    search = False
    
    if request.GET.get('search'):
        search = True
        books = books.filter(title__icontains = request.GET.get('search'))        
    
    qty = len(books)
    print(qty)
    return render(request, "admins/home.html", context={"books": books, "quantity": qty, "search": search, "title": title})
    

def about(request):
    title = "About"
    
    return render(request, "admins/about.html", context = {"title": title})


def contact(request):
    title = "Contact"
    
    return render(request, "admins/contact.html", context = {"title": title})


def admin_login(request):
    title = "Admin Login"
    
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('/admin/home')
    
    # creating admin
    
    # user = Admins.objects.create_user(
    #         name = "Admin",
    #         username = "admin",
    #         password = "admin",
    #     )
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.info(request, "Please fill-out all fields.")
            return render(request, "admins/admin_login.html", context = {"title": title})
        
        login_user = authenticate(username = username, password = password)
        
        if login_user != None:
            login(request, login_user)
            return redirect('/admin/home')
        
        else:
            messages.info(request, "Invalid Username or password.")
            return render(request, "admins/admin_login.html", context = {"title": title})
        
    return render(request, "admins/admin_login.html", context = {"title": title})


@admin_login_required
def admin_logout(request):
    logout(request)
    
    return redirect("/admin/login/")


@admin_login_required
def change_password(request):
    title = "Change Password"
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        if not old_password or not new_password:
            messages.info(request, "Please fill-out all fields.")
            return render(request, "admins/change_password.html", context = {"title": title})
        
        user_name = request.user.username
        print(user_name)
        
        user = Admins.objects.get(username = user_name)
        print(user)
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.info(request, "Password Changed Successfully, Login again.")
            return render(request, "admins/change_password.html", context = {"title": title})
        
        else:
            messages.info(request, "Old Password is Incorrect.!")
            return render(request, "admins/change_password.html", context = {"title": title})
            
    return render(request, "admins/change_password.html", context = {"title": title})


@admin_login_required
def create(request):
    title = "Create Book"
    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        author = data.get('author')
        isbn = data.get('isbn')
        rating = data.get('rating')
        pages = data.get('pages')
        image = request.FILES.get('image')
        pdf = request.FILES.get('pdf')
        
        if image:
            if image.name.lower().endswith(('.png', '.jpeg', '.PNG', '.jpg')):
                image_name = f"{title}.PNG"
                image_path = default_storage.save(f"images/{image_name}", ContentFile(image.read()))
            else:
                messages.info(request, "Your uploaded image file is not in image format.")
                return render(request, "admins/create.html", context = {"title": "Create Book"})
            
        if pdf:
            if pdf.name.lower().endswith('.pdf'):
                pdf_name = f"{title}.pdf"
                pdf_path = default_storage.save(f"pdfs/{pdf_name}", ContentFile(pdf.read()))
            else:
                messages.info(request, "Your uploaded pdf file is not in pdf format.")
                return render(request, "admins/create.html", context = {"title": "Create Book"})

        Books.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            rating=rating,
            pages=pages,
            image=image_path,
            pdf = pdf_path
        )

        return redirect("/")

    return render(request, "admins/create.html", context={"title": title})


@admin_login_required
def delete(request, book_id):
    title = "Delete Book"

    book = Books.objects.filter(id=book_id).first()

    if request.method == "POST":
        book.delete()

        return redirect('/')

    return render(request, "admins/delete.html", context={"book": book, "title": title})


@admin_login_required
def edit(request, book_id):
    title = "Edit Book"
    
    book = Books.objects.filter(id=book_id).first()
    
    if request.method == "POST":
        data = request.POST
        
        image = request.FILES.get('image')
        if image:
            image_name = f"{data.get('title')}.PNG"
            image_path = default_storage.save(f"images/{image_name}", ContentFile(image.read()))
                
        pdf = request.FILES.get('pdf')
        if pdf:
            pdf_name = f"{data.get('title')}.pdf"
            pdf_path = default_storage.save(f"pdfs/{pdf_name}", ContentFile(pdf.read()))

        book.title = data.get('title')
        book.author = data.get('author')
        book.isbn = data.get('isbn')
        book.rating = data.get('rating')
        book.pages = data.get('pages')
        book.image = image_path
        book.pdf = pdf_path
        
        book.save()

        return redirect("/")

    return render(request, "admins/edit.html", context = {"book": book, "title": title})


@admin_login_required
def view(request, book_id):
    title = "View Book"
    
    book = Books.objects.filter(id=book_id).first()
    
    return render(request, "admins/view.html", context = {"book": book, "title": title})
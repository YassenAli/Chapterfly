from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import BookForm, CategoryForm, CheckoutForm, EditBookForm , SignupForm , loginForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages


# Create your views here.

def view(request):
    search = Book.objects.all()
    title = None
    if 'search-name' in request.GET:
        title = request.GET['search-name']
        if title:
            search = search.filter(name__icontains=title)

    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')

    if isLogged is False :
        return redirect('LoginSignup')

    context = {
        'category': Category.objects.all(),
        'books': search,
        'is_admin' : is_admin,
        'isLogged' : isLogged,
    }
    return render(request, 'pages/views.html', context)


def add_book(request):
    if request.method == 'POST':
        if 'add_book' in request.POST:
            add_book = BookForm(request.POST, request.FILES) # request.FILES  to save images
            if add_book.is_valid():
                add_book.save()

        elif 'add_category' in request.POST:
            add_category = CategoryForm(request.POST)
            if add_category.is_valid():
                add_category.save()
        
    context = {
        'form': BookForm(),
        'formCategory': CategoryForm(),
    }
    return render(request, 'pages/add_book.html', context)

def cart(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            return redirect('account')
    context = {
        'form': CheckoutForm(),
    }
    return render(request, 'pages/cart.html', context)

def main(request):
    return render(request, 'pages/main.html')

def account(request):
    #get username
    #get profile picture
    context = { #will be updated after setting a model for acc data
        # 'name' : 'default'
        #'username' : username
        #'profilepic' : profilepic
    }
    return render(request, 'pages/accountUser.html', context)

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('view')  
    else:
        form = EditBookForm(instance=book)
    return render(request, 'pages/edit_book.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('view')
    return render(request, 'pages/delete_book.html', {'book': book})

def details(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponseBadRequest('Book does not exist')

    signup_user_id = request.session.get('user_id')
    if not signup_user_id:
        return HttpResponseBadRequest('User not authenticated')

    try:
        signup_user = Signup.objects.get(id=signup_user_id)
    except Signup.DoesNotExist:
        return HttpResponseBadRequest('User does not exist')

    if request.method == 'POST' and 'add-to-wishlist' in request.POST:
        signup_user.wishlist.add(book)
        return JsonResponse({'status': 'success'})

    is_loved = signup_user.wishlist.filter(id=book.id).exists()

    context = {
        'book': book,
        'is_loved': is_loved
    }
    return render(request, 'pages/details.html', context)


def add_love(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('LoginSignup')
            # return JsonResponse({'status': 'login_required'})

        book_id = request.POST.get('book-id')
        try:
            book = Book.objects.get(id=book_id)
            signup_user = Signup.objects.get(id=request.session.get('user_id'))
        except (Book.DoesNotExist, Signup.DoesNotExist):
            return HttpResponseBadRequest('Book or user does not exist')

        if book in signup_user.wishlist.all():
            return JsonResponse({'status': 'already_in_wishlist'})
        else:
            signup_user.wishlist.add(book)
            return JsonResponse({'status': 'success'})

    return HttpResponseBadRequest()

def wishlist(request):
    context = {
        'wishlist_items': Signup.wishlist.get(user=request.user).wishlist.all(),
    }
    return render(request, 'pages/wishlist.html', context)
    

def get_profile_picture(username):
    user = Signup.objects.get(username=username)
    profile_picture_url = user.profilePicture.url
    return profile_picture_url


def borrow_book(book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.status == 'available':
        book.status = 'borrowed'
        book.save()
        return ('Book successfully borrowed') #update to make it a json response
    else:
        return ('Book is not available for borrowing') #update to make it a json response

def LoginSignup(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            form = SignupForm(request.POST)
            login_form = loginForm()
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('LoginSignup')
        else:
            request.session['isLogged'] = False
            form = SignupForm()
            login_form = loginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['usernameLogin']
                password = login_form.cleaned_data['passwordLogin']
                
                try:
                    signup_user = Signup.objects.get(username=username)
                    if signup_user.password == password: 

                        request.session['user_id'] = signup_user.id 
                        request.session['is_admin'] = signup_user.isAdmin
                        request.session['isLogged'] = True
                        return redirect('view')
                    else:
                        message = 'Invalid username or password'
                except Signup.DoesNotExist:
                    message = 'Invalid username or password'
            else:
                message = 'Form is not valid'
            return render(request, 'pages/LoginSignup.html', {'SignupForm': form, 'loginForm': login_form, 'message': message })
    else:
        form = SignupForm()
        login_form = loginForm()
    return render(request, 'pages/LoginSignup.html', {'SignupForm': form, 'loginForm': login_form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Comment, Forum_Post, User

# -- Restriation and authentication -- #
def register(request):
    if request.method == "GET":
        return redirect('/signup')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/signup')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/signup')
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        messages.error(request, 'Invalid Username/Password')
        return redirect('/signup')
    user = User.objects.get(username=request.POST['username'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

# -- Template renders -- #
def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)

def reviews(request):
    return render(request, 'reviews.html')

def news(request):
    return render(request, 'news.html')

def forum(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'forum_posts': Forum_Post.objects.all()
    }
    return render(request, 'forum.html')

# -- Forum Views -- #
def post_mess(request):
    Forum_Post.objects.create(message=request.POST['mess'], poster = User.objects.get(id=request.session['id']))
    return redirect('/forum')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['id'])
    message = Forum_Post.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, forum_post=message)
    return redirect('/forum')

def add_like(request, id):
    liked_post = Forum_Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

# -- User Profile -- #
def user_profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.username = request.POST['username']
    edit_user.email = request.POST['email']
    edit_user.password = request.POST['password']
    edit_user.save()
    return redirect('/success')
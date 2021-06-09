from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Comment, Forum_Post, User
import requests
# from GamingNews/.env/ import APIKEY
# news_api_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={APIKEY}"

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

# def news(request):
#     r = requests.get(news_api_url)
#     json = r.json()
#     context = {
#         "results": json['results']
#     }
#     return render(request, 'news.html', context=context)

def news(request):
    page = request.GET.get('page', 1)
    # search = request.GET.get('search', None)
    url = f"https://newsapi.org/v2/top-headlines?sources=ign&apiKey={settings.APIKEY}"
    # if search is None or search=="top":
    #     # get the top news
    #     url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
    #         "us",1,settings.APIKEY
    #     )
    r = requests.get(url=url)
    data = r.json()
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        # "search": search
    }
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": "" if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    return render(request, 'news.html', context=context)

# -- Forum Views -- #
def forum(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'forum_posts': Forum_Post.objects.all()
    }
    return render(request, 'forum.html', context)

def post_mess(request):
    Forum_Post.objects.create(post=request.POST['mess'], poster = User.objects.get(id=request.session['user_id']))
    return redirect('/forum')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['user_id'])
    post = Forum_Post.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, forum_post=post)
    return redirect('/forum')

def add_like(request, id):
    liked_post = Forum_Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_post.user_likes.add(user_liking)
    return redirect('/forum')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/forum')

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
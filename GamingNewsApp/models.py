from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['username']) < 4:
            errors['username'] = 'Username must be at least 4 characters'
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        username_check = self.filter(username=form['username'])
        if username_check:
            errors['username'] = "Username already in use"
        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        return errors
    
    def authenticate(self, username, password):
        users = self.filter(username=username)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            username = form['username'],
            email = form['email'],
            password = pw,
        )
        
class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

# Forum
class Forum_Post(models.Model):
    post = models.CharField(max_length=1000)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    forum_post = models.ForeignKey(Forum_Post, related_name='post_comments', on_delete=models.CASCADE)
from django.db import models
from datetime import datetime
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length = 100, unique = True)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.first_name

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
    
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default = datetime.now().date())
    tags = models.ManyToManyField('Tagging', related_name='posts_tags', null = True, blank=True)
    comments = models.ManyToManyField('Comment', related_name = 'post_comments', null = True, blank = True)
    tags_count = models.IntegerField(default = 0, null = True, blank = True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)


    def __str__(self):
        return self.title
        

class Tagging(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post, related_name='tags_posts',null = True, blank=True)

    def __str__(self):
        return self.name
    


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100, unique = True)
    post = models.ManyToManyField(Post, related_name='comments_post')
    content = models.TextField()
    date = models.DateField(default = datetime.now().date())

    def __str__(self):
        return self.name



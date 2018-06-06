from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Author(models.Model):

    authorname = models.CharField(max_length=50)

    authorinfo = models.TextField()

    class Meta:

        db_table='blog_author'

class Articletype(models.Model):

    atname = models.CharField(max_length=50)

    atinfo = models.TextField()

    class Meta:

        db_table='blog_articletype'


class Article(models.Model):

    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    article_type = models.ForeignKey(Articletype,on_delete=models.CASCADE)

    atitle = models.CharField(max_length=200)

    acontent = models.TextField()

    akeep_num = models.IntegerField(default=0)

    apoll_num = models.IntegerField(default=0)

    apub_time = models.DateTimeField(default=datetime.now)

    aupdate_time = models.DateTimeField(default=datetime.now)

    acomment_num = models.IntegerField(default=0)



    class Meta:

        db_table='blog_article'

class Newuser(AbstractUser):

    article = models.ManyToManyField(Article)

    uname = models.CharField(max_length=50)

    upwd = models.CharField(max_length=200)

    uemail = models.CharField(max_length=254)

    uimg = models.ImageField(upload_to='static/images',default='images/default.jpg')

    class Meta:

        db_table = 'blog_newuser'

class Poll(models.Model):

    article = models.ForeignKey(Article,on_delete=models.CASCADE)

    user = models.ForeignKey(Newuser,on_delete=models.CASCADE)

    class Meta:

        db_table = 'blog_poll'

class Comment(models.Model):

    content = models.TextField()

    date = models.DateTimeField(default=datetime.now)

    article = models.ForeignKey(Article,on_delete=models.CASCADE)

    user = models.ForeignKey(Newuser,on_delete=models.CASCADE)

    class Meta:

        db_table = 'blog_comment'

class Keep(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    user = models.ForeignKey(Newuser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'blog_keep'





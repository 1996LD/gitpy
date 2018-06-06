from django.shortcuts import render,redirect
from .forms import RegisterFrom,LoginFrom
from .models import Newuser,Author,Article,Articletype,Keep,Comment,Poll
from django.contrib.auth import login,logout


# Create your views here.

def logoutt(request):

    logout(request)

    return redirect('/login/')

def loginn(request):
    if request.method == "GET":
        return render(request,'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')

        user = Newuser.objects.filter(email=email)
        user = user[0]
        if pwd == user.password:
            login(request,user)

            return redirect('/index/')
        else:
            return render(request,'login.html',{'error':'密码错误'})


def register(request):

    if request.method == 'GET':

        return render(request, 'register.html')

    elif request.method == 'POST':
        # 验证form提交的数据
        form = RegisterFrom(request.POST)
        if form.is_valid():
            # 判断两次密码是否一致
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            rePwd = form.cleaned_data['rePassword']
            # 两次密码不一致
            if pwd != rePwd:
                # 返回注册界面,和错误信息
                return render(request, 'register.html', {'form': form, 'error': '两次密码不一致!'})
            # 判断用户是否存在
            # 根据email查找用户,如果用户存在,返回用户存在的错误信息
            if Newuser.objects.filter(email=email):
                # 用户已存在
                return render(request, 'register.html', {'form': form,
                                                         'errMsg': '该用户已存在!'})
            # 创建用户
            user = Newuser(email=email, password=pwd)
            # 对用户传递过来的密码进行加密,将加密之后的数据进行保存
            # 账户状态 未激活状态
            user.is_active = 1
            user.is_staff = 1
            # 保存为邮箱地址,可以使用邮箱登录后台
            user.username = email
            user.nick_name = ''
            # 保存用户
            user.save()

            author = Author(authorname=email,authorinfo='')
            author.save()

            return redirect('/login/')

        else:
            # 返回form表单
            # 返回注册界面,信息回填,显示错误信息
            return render(request, 'register.html', {'form': form})


def index(request):

    aaa = Article.objects.all()

    a_id = request.user.id

    author = Author.objects.get(id=a_id)

    return render(request,'index.html',{'aaa':aaa,'author':author})



def article(request,y):

    aaa = request.user.id

    article = Article.objects.get(id=y)

    type_id = article.article_type_id

    a_list = Article.objects.filter(article_type_id=type_id)

    if len(a_list) >= 3:
        a_list = a_list[:3]

    comment = Comment.objects.filter(article_id=y)

    if len(comment) >= 3:
        comment = comment[:3]

    if request.method == 'GET':

        return render(request,'article.html',{'article':article,'a_list':a_list,'comment':comment})

    elif request.method == 'POST':

        content = request.POST.get('content')

        con = Comment(content=content,article_id=y,user_id=aaa)

        con.save()

        article.acomment_num = int(article.acomment_num) + 1

        article.save()

        return render(request, 'article.html', {'article': article, 'a_list': a_list, 'comment': comment})


def users(request,x):

    a = request.user.id

    author = Author.objects.get(id=a)

    articles = Article.objects.filter(author_id=a)

    art_num = len(articles)

    if art_num >= 4:

        articles = articles[:4]

    keep = Keep.objects.filter(user_id=a)

    keep_num = len(keep)

    if keep_num >= 4:

        keep = keep[:4]

    comment = Comment.objects.filter(user_id=a)

    com_num = len(comment)

    if com_num >= 4:

        comment = comment[:4]

    if x == 1:

        return render(request, 'users.html',{'author': author, 'art_num': art_num, 'keep_num': keep_num, 'com_num': com_num,'articles': articles, 'keep': keep, 'comment': comment,'aa':x})

    elif x == 2:

        return render(request, 'users.html',{'author': author, 'art_num': art_num, 'keep_num': keep_num, 'com_num': com_num,'articles': articles, 'keep': keep, 'comment': comment,'bb':x})

    elif x == 3:

        return render(request, 'users.html',{'author': author, 'art_num': art_num, 'keep_num': keep_num, 'com_num': com_num,'articles': articles, 'keep': keep, 'comment': comment,'cc':x})

    else:

        return render(request, 'users.html',{'author': author, 'art_num': art_num, 'keep_num': keep_num, 'com_num': com_num,'articles': articles, 'keep': keep, 'comment': comment,'aa':x})


def add_article(request):

    if request.method == 'GET':

        b = request.user.id

        articles = Article.objects.filter(author_id=b)

        art_num = len(articles)

        keep = Keep.objects.filter(user_id=b)

        keep_num = len(keep)

        comment = Comment.objects.filter(user_id=b)

        com_num = len(comment)

        a = request.user.id

        user = Newuser.objects.get(id=a)

        author = Author.objects.get(id=a)

        return render(request,'add-article.html',{'user':user,'author':author,'art_num':art_num,'keep_num':keep_num,'com_num':com_num})

    elif request.method == 'POST':

        atitle = request.POST.get('title')

        acontent = request.POST.get('article')

        sign = request.POST.get('sign')

        try:

            a_type = Articletype.objects.get(atname=sign)

            a_id = a_type.id

        except Exception as e:

            aaa=Articletype(atname=sign,atinfo='')

            aaa.save()

            a_type = Articletype.objects.get(atname=sign)

            a_id = a_type.id

        a = request.user.id

        article = Article(atitle=atitle,acontent=acontent,article_type_id=a_id,author_id=a,acomment_num=0)

        article.save()

        return redirect('/index/')


def poll(request,p):

    a = request.user.id

    try:

        ppp = Poll.objects.get(article_id=p,user_id=a)

        ppp.delete()

        article = Article.objects.get(id=p)

        article.apoll_num = int(article.apoll_num) - 1

        article.save()

    except Exception as e:

        po = Poll(article_id=p, user_id=a)

        po.save()

        article = Article.objects.get(id=p)

        article.apoll_num = int(article.apoll_num) + 1

        article.save()

    return redirect('/article/{}'.format(p))


def keep(request,k):

    a = request.user.id

    try:

        kkk = Keep.objects.get(article_id=k,user_id=a)

        kkk.delete()

        article = Article.objects.get(id=k)

        article.akeep_num = int(article.akeep_num) - 1

        article.save()

    except Exception as e:

        ke = Keep(article_id=k, user_id=a)

        ke.save()

        article = Article.objects.get(id=k)

        article.akeep_num = int(article.akeep_num) + 1

        article.save()

    return redirect('/article/{}'.format(k))


def fabu(request):

    aaa = Article.objects.all().order_by('-apub_time')

    a_id = request.user.id

    author = Author.objects.get(id=a_id)

    return render(request, 'index.html', {'aaa': aaa, 'author': author})


def shoucang(request):

    aaa = Article.objects.all().order_by('-akeep_num')

    a_id = request.user.id

    author = Author.objects.get(id=a_id)

    return render(request, 'index.html', {'aaa': aaa, 'author': author})

def pinglun(request):

    aaa = Article.objects.all().order_by('-acomment_num')

    a_id = request.user.id

    author = Author.objects.get(id=a_id)

    return render(request, 'index.html', {'aaa': aaa, 'author': author})










from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .form import BlogPost

def home(request):
    blogs = Blog.objects.all().order_by('-id')
    #블로그의 모든 글을 대상으로
    blog_list = Blog.objects.all().order_by('-id')
    #블로그 객체 세계를 한 페이지로 자르기
    paginator = Paginator(blog_list,4) #어떤 걸 몇 개씩
    page = request.GET.get('page') #변수에 담기
    posts = paginator.get_page(page)
    return render(request, 'home.html',{'blogs':blogs, 'posts':posts})

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html',{'details':details})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/'+ str(blog.id))

def blogpost(request):
#1. 입력된 내용을 처리하는 기능 -> post
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid(): #잘 입력되어있는지 검사하는 함수
            post = form.save(commit=False) # 아직저장 x
            post.pub_date=timezone.now() #폼에서 입력하지 않은 시간을 등록
            post.save() # 시간을 등록했으면 저장해라
            return redirect('home')
#2. 빈페이지를 띄워주는 기능 -> get
    else:
        form = BlogPost()
        return render(request, 'new.html',{'form':form})
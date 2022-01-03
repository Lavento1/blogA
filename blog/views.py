from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from blog.forms import PostForm
from blog.models import Post


def index(request):
    return render(request, 'blog/index.html')


def post_list(request):
    page = request.GET.get('page', 1)
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page)
    context = {'post_list': page_obj, 'page':page}
    return render(request, 'blog/post_list.html', context)


def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    # post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='common:login')
def post_create(request):
    # 글 쓰기 등록
    if request.method == "POST":
        # 파일이 첨부되어서 오는 경우에는 request.FILES를 추가
        form = PostForm(request.POST, request.FILES)   # 폼에 입력된 자료 가져오기
        if form.is_valid():
            post = form.save(commit=False)  # 가저장
            post.pub_date = timezone.now()
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)


def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()
            post.save()
            return redirect('blog:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)  # instance: 폼에 내용이 채워짐
    context={'form': form}
    return render(request, 'blog/post_form.html', context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()  #질문 삭제
    return redirect('blog:post_list')
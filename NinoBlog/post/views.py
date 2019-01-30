from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .form import PostForm


# Create your views here.

def post_list(request):
    # lte means less than or equals.
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.filter(published_date__isnull=False).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def readmore(request, pk):

    post_more = Post.objects.get(pk=pk)
    comments = post_more.comment.all()
    context ={'post_more': post_more, 'comments': comments, 'count': comments.count()}
    return render(request, 'blog/readmore.html', context)


def form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_draft_list')
    else:
        form_data = PostForm()
    return render(request, 'blog/form.html', {'form': form_data})


def add_comment(request, pk):
    c = Comment()
    post_more = Post.objects.get(pk=pk)
    c.reader = request.POST['comment_name']
    c.post = post_more
    c.text = request.POST['comment']
    c.save()
    return redirect('readmore',pk=pk)


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/Draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('readmore', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def edit(request,pk):
    post = Post.objects.get(pk = pk)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('readmore',pk=pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/form.html', {'form': form})


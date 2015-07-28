import cgi

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET, require_safe
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from rest_framework.renderers import JSONRenderer
from django.conf import settings

from models import Post, Reply
from serializers import PostSerializer, ReplySerializer
from forms import PostForm, ReplyForm


@require_safe
def index(request):
    return render(request, 'home.html')


@require_POST
def add_post(request):
    form = PostForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
    user = request.user
    title = cgi.escape(form.cleaned_data['title'])
    message = cgi.escape(form.cleaned_data['message'])
    post = Post(user=user, title=title, message=message)
    post.save()
    post_data = PostSerializer(post).data
    post_data_json = JSONRenderer().render(post_data)
    return HttpResponse(post_data_json, content_type='application/json')


@require_POST
def add_reply(request, id_):
    form = ReplyForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
    user = request.user
    post = get_object_or_404(Post, pk=id_)
    if not has_post_permission(post, user):
        return HttpResponseForbidden()
    message = cgi.escape(form.cleaned_data['message'])

    reply = Reply(user=user, post=post, message=message)
    reply.save()

    reply_data = ReplySerializer(reply).data
    reply_data_json = JSONRenderer().render(reply_data)
    return HttpResponse(reply_data_json, content_type='application/json')


@require_safe
def get_posts(request):
    user = request.user
    post = Post.objects.all().filter(user=user).order_by('-date')
    post_data = PostSerializer(post, many=True).data
    post_data_json = JSONRenderer().render(post_data)
    return HttpResponse(post_data_json, content_type='application/json')


@require_safe
def get_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if not has_post_permission(post, user):
        return HttpResponseForbidden()
    return render(request, 'post.html', {'post': post})


@require_safe
def get_replies(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if not has_post_permission(post, user):
        return HttpResponseForbidden()
    replies = Reply.objects.all().filter(post=post)
    replies_data_json = JSONRenderer().render(ReplySerializer(replies, many=True).data)
    return HttpResponse(replies_data_json, content_type='application/json')


@require_GET
def get_all_posts(request, offset = 0):
    if request.user.username not in settings.ADMIN_USERNAMES:
        return HttpResponseForbidden()
    offset = int(offset)
    limit = offset + 10
    posts = Post.objects.all().order_by('-date')[offset:limit]
    posts_json = JSONRenderer().render(PostSerializer(posts, many=True).data)
    return HttpResponse(posts_json, content_type='application/json')


@require_GET
def admin_page(request):
    if request.user.username not in settings.ADMIN_USERNAMES:
        return redirect('home:index')
    return render(request, 'admin.html')


def has_post_permission(post, user):
    if user != post.user and user.username not in settings.ADMIN_USERNAMES:
        return False
    return True

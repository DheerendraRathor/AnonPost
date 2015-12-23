import cgi

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET, require_safe
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from rest_framework.renderers import JSONRenderer

from .models import Post, Reply, Site
from .serializers import PostSerializer, ReplySerializer, sanitize_html
from .forms import PostForm, ReplyForm


@require_safe
def index(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = PostForm()
    return render(request, 'home.html', {'site': site, 'form': form})


@require_POST
def add_post(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = PostForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
    user = request.user
    title = cgi.escape(form.cleaned_data['title'])
    message = sanitize_html(form.cleaned_data['message'])
    post = Post(user=user, site=site, title=title, message=message)
    post.save()
    post_data = PostSerializer(post).data
    post_data_json = JSONRenderer().render(post_data)
    return HttpResponse(post_data_json, content_type='application/json')


@require_POST
def add_reply(request, site_id, id_):
    form = ReplyForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
    user = request.user
    post = get_object_or_404(Post, pk=id_, site_id=site_id)
    if not has_post_permission(post, user):
        return HttpResponseForbidden()
    message = sanitize_html(form.cleaned_data['message'])

    reply = Reply(user=user, post=post, message=message)
    reply.save()

    reply_data = ReplySerializer(reply).data
    reply_data_json = JSONRenderer().render(reply_data)
    return HttpResponse(reply_data_json, content_type='application/json')


@require_safe
def get_posts(request, site_id):
    """
    Get all posts of an user of a site
    """
    user = request.user
    site = get_object_or_404(Site, pk=site_id)
    post = Post.objects.all().filter(user=user, site=site).order_by('-created')
    post_data = PostSerializer(post, many=True).data
    post_data_json = JSONRenderer().render(post_data)
    return HttpResponse(post_data_json, content_type='application/json')


@require_safe
def get_post(request, site_id, post_id):
    """
    Get Details of a post
    """
    user = request.user
    post = get_object_or_404(Post, pk=post_id, site_id=site_id)
    reply_form = ReplyForm()
    if not has_post_permission(post, user):
        return HttpResponseForbidden()
    return render(request, 'post.html', {'post': post, 'reply_form': reply_form})


@require_safe
def get_replies(request, site_id, post_id):
    """Get replies of a post"""
    user = request.user
    post = get_object_or_404(Post, pk=post_id, site_id=site_id)
    if not has_post_permission(post, user):
        return HttpResponseForbidden()
    replies = Reply.objects.all().filter(post=post)
    replies_data_json = JSONRenderer().render(ReplySerializer(replies, many=True).data)
    return HttpResponse(replies_data_json, content_type='application/json')


@require_GET
def get_all_posts(request, site_id, offset=0):
    """
    Get all posts of a site (For admin page)
    """
    site = get_object_or_404(Site, pk=site_id)
    if not is_admin(request.user, site):
        return HttpResponseForbidden()
    offset = int(offset)
    limit = offset + 10
    posts = Post.objects.all().filter(site=site).order_by('-created')[offset:limit]
    posts_json = JSONRenderer().render(PostSerializer(posts, many=True).data)
    return HttpResponse(posts_json, content_type='application/json')


@require_GET
def admin_page(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    if not is_admin(request.user, site):
        return redirect('home:index', site_id=site.id)
    return render(request, 'admin.html', {'site': site})


def is_admin(user, site):
    return site.is_demo or user in site.admins.all()


def has_post_permission(post, user):
    return user == post.user or is_admin(user, post.site)

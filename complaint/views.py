from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET, require_safe
from models import Complaint, Reply
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from serializers import ComplaintSerializer, ReplySerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from forms import ComplaintForm, ReplyForm
from django.conf import settings

import cgi

@require_safe
def index(request):
    return render(request, 'home.html')

@require_POST
def add_complaint(request):
    form = ComplaintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
    user = request.user
    title = cgi.escape(form.cleaned_data['title'])
    message = cgi.escape(form.cleaned_data['message'])
    complaint = Complaint(user=user, title=title, message=message)
    complaint.save()
    complaint_data = ComplaintSerializer(complaint).data
    complaint_data_json = JSONRenderer().render(complaint_data)
    return HttpResponse(complaint_data_json, content_type='application/json')

@require_POST
def add_reply(request, id):
    form = ReplyForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')
    user = request.user
    complaint = get_object_or_404(Complaint, pk=id)
    if not has_complaint_permission(complaint, user):
        return HttpResponseForbidden()
    message = cgi.escape(form.cleaned_data['message'])

    reply = Reply(user=user, complaint=complaint, message=message)
    reply.save()

    reply_data = ReplySerializer(reply).data
    reply_data_json = JSONRenderer().render(reply_data)
    return HttpResponse(reply_data_json, content_type='application/json')

@require_safe
def get_complaints(request):
    user = request.user
    complaint = Complaint.objects.all().filter(user=user)
    complaint_data = ComplaintSerializer(complaint, many=True).data
    complaint_data_json = JSONRenderer().render(complaint_data)
    return HttpResponse(complaint_data_json, content_type='application/json')

@require_safe
def get_complaint(request, complaint_id):
    user = request.user
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    if not has_complaint_permission(complaint, user):
        return HttpResponseForbidden()
    return render(request, 'complaint.html', {'complaint' : complaint})

@require_safe
def get_replies(request, complaint_id):
    user = request.user
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    if not has_complaint_permission(complaint, user):
        return HttpResponseForbidden()
    replies = Reply.objects.all().filter(complaint=complaint)
    replies_data_json = JSONRenderer().render(ReplySerializer(replies, many=True).data)
    return HttpResponse(replies_data_json, content_type='application/json')

@require_GET
def get_all_complaints(request, offset):
    if request.user.username not in settings.ADMIN_USERNAMES:
        return HttpResponseForbidden()
    offset = int(offset)
    limit = offset + 10
    complaints = Complaint.objects.all().order_by('-date')[offset:limit]
    complaints_json = JSONRenderer().render(ComplaintSerializer(complaints, many=True).data)
    return HttpResponse(complaints_json, content_type='application/json')

@require_GET
def admin_page(request):
    if request.user.username not in settings.ADMIN_USERNAMES:
        return redirect('/')
    return render(request, 'admin.html')

def has_complaint_permission(complaint, user):
    if user != complaint.user and user.username not in settings.ADMIN_USERNAMES:
        return False
    return True

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET, require_safe
from models import Complaint, Reply
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import HttpResponse, HttpResponseBadRequest
from serializers import ComplaintSerializer, ReplySerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from forms import ComplaintForm
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

# TODO: handle this thing with CGI escape
@require_POST
def add_reply(request, id):
    user = request.user
    complaint = get_object_or_404(Complaint, pk=id)
    message = request.POST.get('message')

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



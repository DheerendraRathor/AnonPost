from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET, require_safe
from models import Complaint, Reply
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import HttpResponse
from serializers import ComplaintSerializer, ReplySerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

@require_safe
def index(request):
    return render(request, 'home.html')

@require_POST
def add_complaint(request):
    message = request.POST.get('message')
    user = request.user

    complaint = Complaint(user=user, message=message)
    complaint.save()
    complaint_data = ComplaintSerializer(complaint).data
    return HttpResponse(complaint_data, content_type='application/json')

@require_POST
def add_reply(request, id):
    user = request.user
    complaint = get_object_or_404(Complaint, pk=id)
    message = request.POST.get('message')

    reply = Reply(user=user, complaint=complaint, message=message)
    reply.save()

    reply_data = ReplySerializers(reply).data
    return HttpResponse(reply_data, content_type='application/json')

@require_safe
def get_complaints(request):
    user = request.user
    complaint = Complaint.objects.all().filter(user=user)
    complaint_data = ComplaintSerializer(complaint, many=True).data
    complaint_data_json = JSONRenderer().render(complaint_data)
    return HttpResponse(complaint_data_json, content_type='application/json')



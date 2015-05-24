__author__ = 'dheerendra'

from rest_framework import serializers
from models import Complaint, Reply

class ReplySerializers(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ('id', 'message')


class ComplaintSerializer(serializers.ModelSerializer):

    replies = ReplySerializers(many=True)

    class Meta:
        model = Complaint
        fields = ('id', 'message', 'replies')
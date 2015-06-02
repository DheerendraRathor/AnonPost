__author__ = 'dheerendra'

from rest_framework import serializers
from models import Complaint, Reply

class ReplySerializer(serializers.ModelSerializer):

    user_type = serializers.SerializerMethodField()

    def get_user_type(self, reply):
        username = reply.user.username
        if (username == "dean.sa"):
            return 'A'
            # Admin User
        else:
            return 'N'
            # Normal User

    class Meta:
        model = Reply
        fields = ('id', 'message', 'user_type')


class ComplaintSerializer(serializers.ModelSerializer):

    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = ('id', 'title', 'message', 'replies')
        depth = 1